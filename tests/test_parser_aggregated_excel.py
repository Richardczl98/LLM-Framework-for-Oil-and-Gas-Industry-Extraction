import unittest
from collections import OrderedDict

from config import TEST_DIR, DATA_DIR
from eval import xls_parser


class TestParserAggregatedExcel(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_aggr_parser_paper(self):
        xls_file = TEST_DIR / 'eval/result/extract_aggr.xlsx'
        want = ['150159', 'Algeria-Non-hydrocarbons_of_significance_in_petroleum_expl',
                'Algeria_Oil_and_gas_industry_strategic_report',
                'On_the_Viscosity_of_Natural_Gases', 'Production_assessment_of_low_production_rate_of_well',
                'iptc-10330-ms', 'iptc-15161-ms', 'iptc-18834-ms', 'otc-26509-ms', 'petsoc-2003-160-ea',
                'petsoc-2006-133', 'spe-115712-ms', 'spe-140630-ms', 'spe-171169-ms', 'spe-179612-ms',
                'spe-182043-ms', 'spe-210009-ms', 'spe-28002-ms', 'spe-30303-ms', 'spe-38298-ms', 'spe-38926-ms',
                'spe-54625-ms', 'spe-63152-ms', 'spe-75199-ms', 'spe-87016-ms', 'spe-9478-pa', 'spe-97733-ms']

        xls = xls_parser.ParseAggregatedExcel(xls_file)
        papers = xls._parse_papers()
        # print(papers)
        assert papers == want

    def test_to_dict_by_paper(self):
        xls_file = TEST_DIR / 'eval/result/extract_aggr.xlsx'
        papers = ['iptc-15161-ms', 'iptc-10330-ms']
        field_display_name = ['Sirikit', 'Marmul Field, Haima West Reservoir', 'Marmul Field, Haima West Reservoir_1',
                              'Marmul Field, Haima West Reservoir_2']

        xls = xls_parser.ParseAggregatedExcel(xls_file)

        assert papers == list(xls.to_dict(papers).keys())

        for fields in xls.to_dict(papers).values():
            for field in fields.keys():
                assert field in field_display_name

    def test_to_dict_by_paper_fields(self):
        xls_file = TEST_DIR / 'eval/result/extract_aggr.xlsx'
        papers = ['iptc-15161-ms', 'iptc-10330-ms']
        fields = ['Sirikit', 'Marmul Field, Haima West Reservoir']

        xls = xls_parser.ParseAggregatedExcel(xls_file)

        assert papers == list(xls.to_dict(papers, fields).keys())

        for fields in xls.to_dict(papers).values():
            for field in fields.keys():
                assert field in fields

