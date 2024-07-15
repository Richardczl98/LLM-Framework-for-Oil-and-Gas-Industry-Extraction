import unittest
from collections import OrderedDict

from config import TEST_DIR, DATA_DIR
from eval import xls_parser


class TestXlsParser(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_xls_parser_no_excel(self):
        pe = xls_parser.ParseExcel()
        print(pe)

    def test_xls_parser(self):
        gt_excel_path = DATA_DIR / 'spe/spe-9478-pa-v2.xlsx'
        pe = xls_parser.ParseExcel(gt_excel_path)
        df = pe.to_dataframe()
        assert len(df['Hewitt Unit']) == 56

    def test_xls_parser_150159(self):
        gt_excel_path = DATA_DIR / 'others/150159-RZ.xlsx'
        pe = xls_parser.ParseExcel(gt_excel_path)
        print(pe._parse_oil_fields())
        # assert df['Hewitt Unit'] == 0

    def test_split_block_with_all_block(self):
        text = '49 300 thous. tons@Reference page 3 and content, "Accumulated oil production is 49 300 thous. tons," | not_mentioned | 58 003.6 thous.m3@This is the beginning of page 14. Cumulative oil production by the model is 58 003.6 thous.m3'
        max_block = 3
        want = ['49 300 thous. tons@Reference page 3 and content, "Accumulated oil production is 49 300 thous. tons,"', 'not_mentioned', '58 003.6 thous.m3@This is the beginning of page 14. Cumulative oil production by the model is 58 003.6 thous.m3']
        assert xls_parser._split_block(text, max_block) == want

    def test_split_block_with_partical_block(self):
        text = 'not_mentioned'
        max_block = 3
        want = ['not_mentioned', 'not_mentioned', 'not_mentioned']
        assert xls_parser._split_block(text, max_block) == want

    def test_xls_parser_210009(self):
        gt_excel_path = DATA_DIR / 'spe/spe-210009-ms-v2.xlsx'
        pe = xls_parser.ParseExcel(gt_excel_path)
        print(pe.fields)
        print(pe.fields_display)
        print(pe.to_dict(into=OrderedDict))

    def test_xls_parser_1179612(self):
        gt_excel_path = DATA_DIR / 'spe/spe-179612-ms-v2.xlsx'
        pe = xls_parser.ParseExcel(gt_excel_path)
        print(pe.to_dataframe())


class TestRawExcelParser(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_parse_extract_fields(self):
        raw_excel = TEST_DIR / 'eval/result/240215_2057-gpt-4-section/extract_raw.xlsx'
        pe = xls_parser.ParseEvaluationExcel(raw_excel)
        got = pe._extract_blocks()
        want = ['Bayu', 'Undan', 'North Rankin', 'Goodwyn', 'Pluto', 'Xena', 'Coal seam gas',
                'Gorgon', 'Io', 'Jansz', 'Wheatstone', 'Iago', 'Ichthys', 'Prelude', 'Concerto',
                'Pluto_1', 'Scarborough', 'Torosa', 'Brecknock', 'Calliance']
        assert list(got.keys()) == want

    def test_parse_raw_properties(self):
        raw_excel = TEST_DIR / 'eval/result/240215_2057-gpt-4-section/extract_raw.xlsx'
        pe = xls_parser.ParseEvaluationExcel(raw_excel)
        # got = pe._make_raw_properties()
        got = pe._extract_blocks()

        print(got['Coal seam gas']['block_1'])
        want = ['Bayu', 'Undan', 'North Rankin', 'Goodwyn', 'Pluto', 'Xena', 'Coal seam gas',
                'Gorgon', 'Io', 'Jansz', 'Wheatstone', 'Iago', 'Ichthys', 'Prelude', 'Concerto',
                'Pluto_1', 'Scarborough', 'Torosa', 'Brecknock', 'Calliance']

        #