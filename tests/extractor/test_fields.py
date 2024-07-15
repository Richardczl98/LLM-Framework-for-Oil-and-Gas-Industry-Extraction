import unittest

from config import DATA_DIR
from schema.fields import field_list
from eval import xls_parser


class TestFieldCollection(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_set_field_list_by_name(self):
        data = {
            'North Dome': [1996, 2014, 2012],
            'South Pars': [2013],
            'Golshan': [],
            'Ferdowsi': [],
        }
        want = 6
        field_list.set_field_list_by_name(data)
        print(field_list)
        assert len(field_list.field_list) == want

    def test_set_field_list_from_gt(self):
        gt_excel_path = DATA_DIR / 'others/150159_122923_RZ.xlsx'
        want = 7
        pe = xls_parser.ParseExcel(gt_excel_path)
        field_list.set_field_list_from_gt(pe)
        print(field_list)
        assert len(field_list.field_list) == want


