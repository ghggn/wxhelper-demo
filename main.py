import asyncio
import logging

import qasync
from PySide6 import QtWidgets

import server_and_client
from ui import MainWindow, UILogging

TEXT_PROC = {
    "name": "python.exe",
    "prefix": "Python"
}

DEFAULT_PROC = {
    "name": "wechat.exe",
    "prefix": "微信"
}

BOT_CONFIG = {
    "port": 11000
}


def main():
    app = QtWidgets.QApplication()
    main_window = MainWindow(DEFAULT_PROC, BOT_CONFIG)
    m_log = UILogging(main_window.sig)
    m_log.setFormatter(logging.Formatter("%(asctime)s - %(message)s", datefmt="%y.%m.%d %H:%M:%S"))
    logging.getLogger().addHandler(m_log)
    logging.getLogger().setLevel(logging.INFO)
    main_window.sig.connect(main_window.log_to_window)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    asyncio.gather(server_and_client.main(BOT_CONFIG))
    main_window.ui.window.show()
    logging.info("Starting")

    loop.run_forever()


async def test_interval_log():
    i = 0
    while True:
        logging.info("interval -- {}".format(i))
        i += 1
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    main()
