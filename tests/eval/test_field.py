import unittest

from pathlib import Path
from config import DATA_DIR
from eval import xls_parser


class TestField(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_get_producing_year_for_dup_field(self):
        gt_excel_path = Path(DATA_DIR, 'spe/spe-140630-ms-v2.xlsx')
        pe = xls_parser.ParseExcel(gt_excel_path)
        want = [1965, 2010]
        for field, want_year in zip(pe.fields, want):
            assert field.get_producing_year() == want_year

    def test_get_producing_year(self):
        gt_excel_path = Path(DATA_DIR, 'spe/spe-115712-ms-v2.xlsx')
        pe = xls_parser.ParseExcel(gt_excel_path)
        want = None
        for field in pe.fields:
            assert field.get_producing_year() is want
