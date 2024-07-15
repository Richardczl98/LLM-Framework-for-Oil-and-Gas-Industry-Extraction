import unittest

from config import RESULT_DIR
from lib.file_op import get_last_dir


class TestGetLastDir(unittest.TestCase):
    def setUp(self) -> None:
        print('/n')

    def test_get_last_dir(self):
        filepath = RESULT_DIR
        print(get_last_dir(str('result/iptc-10330-ms')))
