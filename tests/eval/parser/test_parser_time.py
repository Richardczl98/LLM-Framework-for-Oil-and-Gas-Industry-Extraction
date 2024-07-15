import unittest

from eval.parser.parser_time import ParserTime
import numpy as np


class TestParserTime(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_parser_time(self):
        data = [
            '23 years',
            '17 million barrels from 1984 to 1999, 160 million barrels expected if the flank waterflooding continues until 2019@The paper concludes...from 1984 to 1999. A net oil recovery of 160 million barrels is expected...until 2019',
            'Increased from 753 psia in 1984 to 950 psia in 1999 due to water injection@The average reservoir pressure increased from 753 psia in 1984 to 950 psia in 1999 in response to the water injection']

        for item in data:
            rst = ParserTime().parse(item)
            print(rst.data)
            print(rst.error)
            print(rst.data.value)

        data = ["Not mentioned", "not_mentioned", "not_mentioned"]
        for item in data:
            rst = ParserTime().parse(item, unit='bbl water/bbl oil')
            assert rst.data.value == np.nan
