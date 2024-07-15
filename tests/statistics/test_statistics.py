import unittest
from lib.file_op import generate_summary_csv


class StatisticsTestCase(unittest.TestCase):
    def test_generate_summary_csv(self):
        result = generate_summary_csv('result')
        self.assertEqual(True, result)  # add assertion here


if __name__ == '__main__':
    unittest.main()
