from dataclasses import dataclass


@dataclass
class ProcessInfo:
    pid: int
    name: str
    is_inject: bool
    is_login: bool
    is_enable_msg_callback: bool
    login_user_name: str
    inject_dll_bind_port: int
