import unittest

import numpy as np

from eval.parser.parser_mention import ParserMentioned


class TestParserMentioned(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_mentioned_value(self):
        data = 'mentioned@This is the beginning of page 6 pattern allocations are being used to set injection volumes.'

        pm = ParserMentioned()
        get = pm.parse(data)
        print(get.data.value)
        print(type(get.data.value))

    def test_not_mentioned_value(self):
        data = 'not_mentioned'

        pm = ParserMentioned()
        get = pm.parse(data)
        print(get.data.value)
        print(type(get.data.value))

    def test_not_mentioned_value2(self):
        data = ["Not mentioned", "not_mentioned", "not_mentioned"]
        for item in data:
            rst = ParserMentioned().parse(item, unit='bbl water/bbl oil')
            assert rst.data.value == np.nan

