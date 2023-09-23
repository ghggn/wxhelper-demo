import asyncio
import json
import logging

import aiohttp

BASE_URL = "http://localhost"
API_CHECK_LOGIN = "/api/checkLogin"
API_GET_LOGIN_USER_INFO = "/api/userInfo"
API_HOOK_MSG = "/api/hookSyncMsg"


class Client:
    @staticmethod
    async def is_login(port: int) -> bool:
        async with aiohttp.ClientSession(base_url="{}:{}".format(BASE_URL, port)) as session:
            async with session.post(API_CHECK_LOGIN) as resp:
                date = await resp.json()
                return date["code"] == 1

    @staticmethod
    async def get_login_user_info(port: int) -> dict:
        async with aiohttp.ClientSession(base_url="{}:{}".format(BASE_URL, port)) as session:
            async with session.post(API_GET_LOGIN_USER_INFO) as resp:
                return await resp.json()

    @staticmethod
    async def hook_msg(bot_tcp_port: int, wxhelper_port: int) -> bool:
        body = {"port": bot_tcp_port, "ip": "127.0.0.1", "url": "http://localhost:8080", "timeout": "3000", "enableHttp": "0"}
        headers = {"Content-Type": "application/json"}

        async with aiohttp.ClientSession(base_url="{}:{}".format(BASE_URL, wxhelper_port)) as session:
            async with session.post(API_HOOK_MSG, json=body, headers=headers) as resp:
                date = await resp.json()
                return date["code"] == 0


class Server:
    def __init__(self, port: int):
        self.port = port
        self.server: asyncio.Server = None
        pass

    async def run(self):
        self.server = await asyncio.start_server(self.handle, "127.0.0.1", self.port)
        logging.info("TCP服务器启动,监听地址为:127.0.0.1:{}".format(self.port))
        async with self.server:
            await self.server.serve_forever()

    async def handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        date = await reader.read()
        try:
            data_json_dict = json.loads(date.decode("utf-8"))
            if "type" in data_json_dict and data_json_dict["type"] == 1:
                logging.info("{} - {}".format(data_json_dict["fromUser"], data_json_dict["content"]))
                pass

        except json.JSONDecodeError:
            pass


async def main(bot_config: dict):
    await Server(bot_config["port"]).run()
