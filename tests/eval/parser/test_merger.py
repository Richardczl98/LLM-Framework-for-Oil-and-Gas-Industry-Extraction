import unittest
import numpy as np
from collections import OrderedDict

from eval.merger.merge_by_block import merge_by_block
from eval.merger.merger import Merger
from eval.parser.parser_result import ParserData, ParserSuccessResult, SUCCESS, ERROR
from eval.parser.parser_mention import ParserMentioned
from eval.parser.parser_unit import ParserUnit
from eval.parser.parser_response import ParserResponse
from schema.variables import Variable


class TestMergeByBlock(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_merge_by_block_1(self):
        variable = Variable(name="Water reinjection", section='Production methods', value_parser=ParserMentioned, merger=Merger)
        data = [
            ParserResponse(
                field='test',
                result=ParserSuccessResult(data=ParserData(value=1.0), status=ERROR),
                section='Production methods',
                record='{Water reinjection:mentioned@This is the beginning of page 6 pattern allocations are being used to set injection volumes.}',
                raw_text='mentioned@This is the beginning of page 6 pattern allocations are being used to set injection volumes.',
                variable=variable,
            ),
            ParserResponse(
                field='test',
                section='Production methods',
                record='{Water reinjection:not_mentioned}',
                result=ParserSuccessResult(data=ParserData(value=np.nan), status=SUCCESS),
                raw_text='{not_mentioned}',
                variable=variable,
            ),
        ]
        want = OrderedDict([('Water reinjection', [1.0, None, None, 'mentioned@This is the beginning of page 6 pattern allocations are being used to set injection volumes. | {not_mentioned}', 'error'])])
        got = merge_by_block(data)
        assert got == want

    def test_merge_by_block_2(self):
        variable = Variable(name="Water reinjection", section='Production methods', value_parser=ParserMentioned, merger=Merger)
        data = [
            ParserResponse(
                field='test',
                result=ParserSuccessResult(data=ParserData(value=np.nan)),
                section='Production methods',
                record='{Water reinjection:mentioned@This is the beginning of page 6 pattern allocations are being used to set injection volumes.}',
                raw_text='mentioned@This is the beginning of page 6 pattern allocations are being used to set injection volumes.',
                variable=variable,
            ),
            ParserResponse(
                field='test',
                section='Production methods',
                record='{Water reinjection:not_mentioned}',
                result=ParserSuccessResult(data=ParserData(value=1.0)),
                raw_text='{not_mentioned}',
                variable=variable,
            ),
        ]
        want = OrderedDict([('Water reinjection', [1.0, None, None, 'mentioned@This is the beginning of page 6 pattern allocations are being used to set injection volumes. | {not_mentioned}'])])
        got = merge_by_block(data)
        assert got == want


    def test_merge_none_value(self):
        variable = Variable(name="Water reinjection", section='Production methods', value_parser=ParserMentioned, merger=Merger)
        data = [
            ParserResponse(
                field='test',
                result=ParserSuccessResult(data=ParserData()),
                section='Production methods',
                record='{Water reinjection:mentioned@This is the beginning of page 6 pattern allocations are being used to set injection volumes.}',
                raw_text='mentioned@This is the beginning of page 6 pattern allocations are being used to set injection volumes.',
                variable=variable,
            ),
            ParserResponse(
                field='test',
                section='Production methods',
                record='{Water reinjection:not_mentioned}',
                result=ParserSuccessResult(data=ParserData(value=1.0)),
                raw_text='not_mentioned',
                variable=variable,
            ),
        ]
        want = OrderedDict([('Water reinjection', [1.0, None, None, 'mentioned@This is the beginning of page 6 pattern allocations are being used to set injection volumes. | not_mentioned'])])
        got = merge_by_block(data)
        # print(got)
        # print(want)
        assert got == want


    def test_merge_string_value(self):
        variable = Variable(name="Water reinjection", section='Production methods', value_parser=ParserMentioned, merger=Merger)
        data = [
            ParserResponse(
                field='test',
                result=ParserSuccessResult(data=ParserData(value='mentioned', unit = '', ref='This is the beginning of page 6 pattern allocations are being used to set injection volumes.')),
                section='Production methods',
                record='{Water reinjection:mentioned@This is the beginning of page 6 pattern allocations are being used to set injection volumes.}',
                raw_text='mentioned@This is the beginning of page 6 pattern allocations are being used to set injection volumes.',
                variable=variable,
            ),
            ParserResponse(
                field='test',
                section='Production methods',
                record='{Water reinjection:not_mentioned}',
                result=ParserSuccessResult(data=ParserData(value='not_mentioned', unit='')),
                raw_text='not_mentioned',
                variable=variable,
            ),
        ]
        want = OrderedDict([('Water reinjection', ['mentioned | not_mentioned', '', 'This is the beginning of page 6 pattern allocations are being used to set injection volumes.', 'mentioned@This is the beginning of page 6 pattern allocations are being used to set injection volumes. | not_mentioned'])])

        got = merge_by_block(data)
        # print(got)
        # print(want)
        assert got == want

    def test_merge_value_and_not_mentioned(self):
        variable = Variable(name='Reservoir permeability', section='Others', unit='mD', value_parser=ParserUnit,
                            merger=Merger, gt_row=82)
        data = [
            ParserResponse(
                field='test',
                result=ParserSuccessResult(
                    data=ParserData(
                        value=723, unit='md',
                        ref='Page 3, "Average permeability, md ",723'
                    )
                ),
                section='Others',
                record='{Reservoir permeability:723 md@Page 3, "Average permeability, md ",723}',
                raw_text='723 md@Page 3, "Average permeability, md ",723',
                variable=variable,
            ),
            ParserResponse(
                field='test',
                section='Others',
                record='Reservoir permeability:not_mentioned',
                result=ParserSuccessResult(data=ParserData(value=np.nan, unit='')),
                raw_text='not_mentioned',
                variable=variable,
            ),
        ]
        want = OrderedDict(
            [('Reservoir permeability',
              [723, 'md', 'Page 3, "Average permeability, md ",723',
                '723 md@Page 3, "Average permeability, md ",723 | not_mentioned'])])

        got = merge_by_block(data)

        assert got == want
