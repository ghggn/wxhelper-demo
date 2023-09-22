import json
import os.path
from subprocess import check_output
from typing import Tuple

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
    if not os.path.exists("injector.exe") or not os.path.exists("wxhelper.dll"):
        return False, "未找到必要的文件 inject.exe或wxhelper.dll"
    res = check_output(["injector.exe", "-p", str(pid), "-i", DLL_NAME]).decode("gbk").strip()
    if res.find("Successfully") == -1:
        return False, "注入失败:\n{}".format(res)
    return True, "注入成功:\n{}".format(res)


def eject_dll_by_pid(pid: int) -> Tuple[bool, str]:
    if not os.path.exists("injector.exe") or not os.path.exists("wxhelper.dll"):
        return False, "未找到必要的文件 inject.exe或wxhelper.dll"
    res = check_output(["injector.exe", "-p", str(pid), "-e", DLL_NAME]).decode("gbk").strip()
    if res.find("Successfully") == -1:
        return False, "取消注入失败:\n{}".format(res)
    return True, "取消注入成功:\n{}".format(res)


def write_config_file(port: int, wx_path) -> bool:
    config_path = os.path.join(wx_path, "config.ini")
    try:
        with open(config_path, "w") as f:
            f.write("[config]\n")
            f.write("port={}\n".format(port))
            return True
    except Exception as e:
        print(e)
        return False


def is_dll_already_inject(pid: int, dll_name=DLL_NAME) -> bool:
    if not psutil.pid_exists(pid):
        return False
    proc = psutil.Process(pid)
    for dll in proc.memory_maps():
        if dll.path.lower().find(dll_name) != -1:
            print(dll.path)
            return True
    return False


def save_proc_infos(procs: list[ProcessInfo], path: str = PROC_INFOS_FILE_NAME):
    # save procs as json file
    with open(path, "w") as f:
        f.write(json.dumps(procs, default=lambda o: o.__dict__, sort_keys=True, indent=4))


def load_proc_infos(path: str = PROC_INFOS_FILE_NAME) -> list[ProcessInfo]:
    # load procs from json file
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        dict_list = json.loads(f.read())
        res = []
        for item in dict_list:
            res.append(ProcessInfo(**item))
        print(res)
        print(dict_list)
        return res
