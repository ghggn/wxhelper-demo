import asyncio
import logging
import os.path

from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, Signal, QObject
from PySide6.QtWidgets import QFileDialog, QMessageBox, QMainWindow

import ui_main
import utils
from models import ProcessInfo
from server_and_client import Client


class UILogging(logging.Handler):
    def __init__(self, sig: Signal):
        super().__init__()
        self.sig = sig

    def emit(self, record):
        msg = self.format(record)
        self.sig.emit(msg)


class ProcModel(QAbstractListModel):
    def __init__(self, proc_infos, proc_dic):
        super().__init__()
        self.procs: list[ProcessInfo] = proc_infos
        self.proc_dic = proc_dic

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            proc = self.procs[index.row()]
            return "{}[{}]\n登陆用户({})\n进程ID({})\n绑定端口({})".format(
                self.proc_dic["prefix"], "消息回调已启用" if proc.is_enable_msg_callback else "消息回调未启用", proc.login_user_name, proc.pid, proc.inject_dll_bind_port
            )

    def rowCount(self, index):
        return len(self.procs)


class MainWindow(QObject):
    is_wx_path_set = False
    auto_increase_port = 12000
    wx_dir = ""
    sig = Signal(str)

    def __init__(self, proc_dic: dict, bot_config: dict):
        super().__init__()

        ui_main_windows = ui_main.Ui_main_window()
        ui_main_windows.setupUi(QMainWindow())
        ui = ui_main_windows
        ui.window.setWindowFlags(Qt.WindowType.MSWindowsFixedSizeDialogHint)
        ui.window.closeEvent = self.close_windows
        ui.refresh_procs_bt.clicked.connect(self.refresh_proc_list_signal)
        ui.list_view.clicked.connect(self.list_item_click_signal)
        ui.inject_dll_bt.clicked.connect(self.inject_dll_signal)
        ui.select_wx_path_bt.clicked.connect(self.set_wx_path_signal)
        ui.sync_login_status_bt.clicked.connect(self.sync_login_status_signal)
        ui.enable_msg_callback.clicked.connect(self.enable_msg_callback_signal)

        ui.log_area.setReadOnly(True)
        ui.clean_log_bt.clicked.connect(self.clean_log_signal)

        self.ui = ui
        self.proc_dic = proc_dic
        self.bot_config = bot_config

        model = ProcModel(self.init_procs(), proc_dic)
        ui.list_view.setModel(model)

    def init_procs(self) -> list[ProcessInfo]:
        current_proc_list = utils.get_process_id_by_name(self.proc_dic["name"])
        saved_proc_list = utils.load_proc_infos()
        if not saved_proc_list:
            return current_proc_list
        for old_proc in saved_proc_list:
            for new_p in current_proc_list:
                if old_proc.is_inject and old_proc.pid == new_p.pid:
                    new_p.is_inject = True
                    new_p.inject_dll_bind_port = old_proc.inject_dll_bind_port
                    new_p.is_login = old_proc.is_login
                    new_p.login_user_name = old_proc.login_user_name
                    new_p.is_enable_msg_callback = old_proc.is_enable_msg_callback
        return current_proc_list

    def log_to_window(self, msg):
        self.ui.log_area.document().size().width()
        self.ui.log_area.appendPlainText(msg)

    def clean_log_signal(self):
        self.ui.log_area.clear()

    def list_item_click_signal(self, item):
        proc = item.model().procs[item.row()]
        self.ui.proc_id_label.setText(str(proc.pid))
        self.ui.inject_statu_label.setText("DLL已注入" if proc.is_inject else "未知")
        self.ui.login_user_name_label.setText(proc.login_user_name)
        self.ui.bind_prot_label.setText(str(proc.inject_dll_bind_port))
        self.ui.sync_login_status_bt.setEnabled(proc.is_inject and not proc.is_login)
        self.ui.inject_dll_bt.setEnabled(not proc.is_inject)
        self.ui.enable_msg_callback.setEnabled(proc.is_inject and not proc.is_enable_msg_callback)

    def close_windows(self, e):
        self.ui.window.close()
        asyncio.get_event_loop().stop()
        asyncio.get_event_loop().close()

    def refresh_proc_list_signal(self):
        new_processes = utils.get_process_id_by_name(self.proc_dic["name"])
        final_proc: list[ProcessInfo] = []
        for old_proc in self.ui.list_view.model().procs:
            for new_p in new_processes:
                if old_proc.pid == new_p.pid:
                    new_processes.remove(new_p)
                    final_proc.append(old_proc)
        final_proc.extend(new_processes)
        new_model = ProcModel(final_proc, self.proc_dic)
        self.ui.list_view.setModel(new_model)

    def set_wx_path_signal(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self.ui.window, "选择微信路径", "", "微信文件(wechat.exe)")
        if not file_path:
            return
        self.wx_dir = os.path.dirname(file_path)
        self.ui.wx_path_label.setText(file_path)
        self.is_wx_path_set = True

    def inject_dll_signal(self):
        """DLL注入 注入前先检测微信路径是否设置,然后写入端口号到config.ini,并同步到界面元素"""
        prefix = "[{}]失败\n".format(self.ui.inject_dll_bt.text())
        if self.ui.proc_id_label.text() == "0":
            self.toast("{}请先选择一个进程".format(prefix))
            return
        if not self.is_wx_path_set:
            self.toast("{}请先设置微信路径".format(prefix))
            return
        c_item, proc = self.get_item_proc()
        if not c_item.model():
            self.toast("{}请先选择一个进程".format(prefix))
            return
        print(proc)
        is_success = utils.write_config_file(self.auto_increase_port, self.wx_dir)
        if not is_success:
            self.toast("{}config.ini写入失败".format(prefix))
            return
        # 注入DL
        is_success, res_str = utils.inject_dll_by_pid(proc.pid)
        if not is_success:
            self.toast("{}{}".format(prefix, res_str))
            return
        proc.is_inject = True
        proc.inject_dll_bind_port = self.auto_increase_port
        self.auto_increase_port += 1
        self.ui.inject_dll_bt.setEnabled(False)
        logging.info("DLL注入成功,进程ID:{}".format(proc.pid))
        self.ui.list_view.clicked.emit(c_item)
        utils.save_proc_infos(c_item.model().procs)

    def enable_msg_callback_signal(self):
        asyncio.gather(self.enable_msg_callback())

    async def enable_msg_callback(self):
        c_item, proc = self.get_item_proc()
        b = await Client.hook_msg(self.bot_config["port"], proc.inject_dll_bind_port)
        if not b:
            self.toast("消息回调失败,请稍后重试")
        proc.is_enable_msg_callback = b
        self.ui.list_view.clicked.emit(c_item)
        logging.info("启用消息回调成功,进程ID{}".format(proc.pid))
        utils.save_proc_infos(c_item.model().procs)

    def sync_login_status_signal(self):
        asyncio.gather(self.sync_login_status())

    async def sync_login_status(self):
        c_item, proc = self.get_item_proc()
        port = self.ui.bind_prot_label.text()
        is_login = await Client.is_login(int(port))
        if not is_login:
            self.toast("该微信进程没有登陆,请先登陆再操作")
            return
        data = await Client.get_login_user_info(int(port))
        if data["code"] != 1:
            self.toast("同步用户信息失败,请稍后重试")
            return
        proc.login_user_name = data["data"]["name"]
        proc.is_login = True
        self.ui.login_user_name_label.setText(data["data"]["name"])
        c_item.user_info = data["data"]
        self.ui.list_view.clicked.emit(c_item)
        logging.info("同步用户信息成功")
        utils.save_proc_infos(c_item.model().procs)

    def get_item_proc(self) -> tuple[QModelIndex, ProcessInfo | None]:
        c_item = self.ui.list_view.currentIndex()
        proc = c_item.model().procs[c_item.row()] if c_item.model() else None
        return c_item, proc

    def toast(self, msg):
        QMessageBox.information(self.ui.window, "提示", msg)
