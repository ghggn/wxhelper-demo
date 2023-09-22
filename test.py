import unittest

import server_and_client
import utils


class MyTest(unittest.TestCase):
    def test_something(self):
        inject = utils.is_dll_already_inject(752, "wxhelper.dll")
        self.assertEqual(True, inject)
        pass

    async def test_msg_callback(self):
        r_b = await server_and_client.Client.hook_msg(11000, 12000)
        self.assertEqual(True, r_b)
        pass


def temp_test():
    utils.is_dll_already_inject(6852)


if __name__ == "__main__":
    temp_test()
