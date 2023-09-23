import json
import logging
import os.path
from subprocess import check_output
from typing import Tuple
import pymem

import psutil

from models import ProcessInfo

DLL_NAME = "wxhelper.dll"
PROC_INFOS_FILE_NAME = "proc_infos.json"


def get_process_id_by_name(process_name):
    res_list: list[ProcessInfo] = []
    for item in psutil.process_iter():
        if process_name == item.name().lower():
            pro_info = ProcessInfo(pid=item.pid, name=process_name, is_inject=False, is_login=False, is_enable_msg_callback=False, login_user_name="暂未获取", inject_dll_bind_port=0)
            res_list.append(pro_info)
    return res_list


def inject_dll_by_pid(pid: int) -> Tuple[bool, str]:
    if is_dll_already_inject(pid):
        return True, "该进程已经注入过了"
    if not os.path.exists("wxhelper.dll"):
        return False, "未找到必要的文件:wxhelper.dll"
    pm = pymem.Pymem()
    try:
        pm.open_process_from_id(pid)
        pymem.pymem.process.inject_dll(pm.process_handle, bytes(os.path.abspath("wxhelper.dll"), encoding="ascii"))
        is_inject = is_dll_already_inject(pid)
        if not is_inject:
            return False, "注入失败,可能权限不足或其他未知错误"
        return True, "注入成功"
    except Exception as e:
        return False, "注入失败.{}".format(e)


def write_config_file(port: int, wx_path) -> bool:
    config_path = os.path.join(wx_path, "config.ini")
    try:
        with open(config_path, "w") as f:
            f.write("[config]\n")
            f.write("port={}\n".format(port))
            return True
    except Exception as e:
        logging.error("写入config.ini失败:{}".format(e))
        return False


def is_dll_already_inject(pid: int, dll_name=DLL_NAME) -> bool:
    if not psutil.pid_exists(pid):
        return False
    proc = psutil.Process(pid)
    for dll in proc.memory_maps():
        if dll.path.lower().find(dll_name) != -1:
            return True
    return False


def save_proc_infos(procs: list[ProcessInfo], path: str = PROC_INFOS_FILE_NAME) -> bool:
    # save procs as json file
    try:
        with open(path, "w") as f:
            f.write(json.dumps(procs, default=lambda o: o.__dict__, sort_keys=True, indent=4))
        return True
    except Exception as e:
        logging.error("保存进程信息失败:{}".format(e))
        return False


def load_proc_infos(path: str = PROC_INFOS_FILE_NAME) -> list[ProcessInfo]:
    # load procs from json file
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        dict_list = json.loads(f.read())
        res = []
        for item in dict_list:
            res.append(ProcessInfo(**item))
        return res
