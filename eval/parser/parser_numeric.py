"""
Author: Alex <alex.hu@57blocks.com>
Date Created: 2023-10-19
Description: Numeric parser class.
"""

from .parser_utils import *
from .parser import Parser
from typing import Any
from lib.helper import split_at_first_char
from .parser_result import ParseResult, ParserErrorResult, ParserSuccessResult

pattern_first_number = r'(\d[\d,\.]*\d?)'


class ParserNumeric(Parser):

    @handle_parser_error
    def parse(self, content: Any, key=None, unit=None) -> ParseResult:
        parse_content = split_at_first_char(content, SPLIT_REF_CHAR)
        parse_content = super().remove_qutoes(parse_content)
        parse_content = super().remove_commas(parse_content)

        cls_name = (type(self).__name__)

        if is_not_mentioned(parse_content[0]):
            parse_content[0] = np.nan
            return ParserSuccessResult.handle_success_response(content, parse_content, class_name=cls_name)

        match = re.search(pattern_first_number, parse_content[0])
        if match:
            data = match.group().replace(',', '')
            parse_content[0] = data
            if not is_number(parse_content[0]):
                return ParserErrorResult.handle_err_response(content, parse_content, class_name=cls_name)
        else:
            parse_content[0] = word_to_number(parse_content[0])
            #word to number error
            if not is_number(parse_content[0]) or parse_content[0] <= 0:
                return ParserErrorResult.handle_err_response(content, parse_content, class_name=cls_name)

        parse_content[0] = float(parse_content[0])
        return ParserSuccessResult.handle_success_response(content, parse_content, class_name=cls_name)

