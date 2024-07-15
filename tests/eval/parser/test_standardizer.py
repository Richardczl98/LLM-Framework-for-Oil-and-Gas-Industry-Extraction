import unittest

from eval import standardizer as sd


class TestStandardizer(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_handle_re_extract_llm(self):
        reference = ''
