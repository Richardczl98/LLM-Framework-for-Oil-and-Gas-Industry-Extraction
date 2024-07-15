"""
Author: Alex <alex.hu@57blocks.com>
Date Created: 2023-10-19
Description: Time parser class.
"""
import re

from .parser import Parser
from typing import Any
from .parser_utils import handle_parser_error, is_not_mentioned, SPLIT_REF_CHAR
from lib.helper import split_at_first_char
from .parser_result import ParseResult, ParserSuccessResult, ParserErrorResult
from datetime import datetime
import numpy as np
from config import YEAR_FOR_CALUCULATION

pattern_year = re.compile(r'(\d{4})')
pattern_number = r'([\d,]*\.\d+|[\d,]+)\s*(\S*)'


class ParserTime(Parser):
    @handle_parser_error
    def parse(self, content:Any, key=None, unit=None) -> ParseResult:
        parse_content = split_at_first_char(content, SPLIT_REF_CHAR)

        cls_name = (type(self).__name__)

        if is_not_mentioned(parse_content[0]):
            parse_content[0] = np.nan
            return ParserSuccessResult.handle_success_response(content, parse_content, class_name=cls_name)

        match = pattern_year.search(parse_content[0])
        if match:
            year = match.group(1)
            difference = YEAR_FOR_CALUCULATION - int(year)
            parse_content[0] = difference
        else:
            match = re.search(pattern_number, parse_content[0])
            if not match:
                return ParserErrorResult.handle_err_response(content, parse_content, class_name=cls_name)

            parse_content[0] = match.groups()[0]

        return ParserSuccessResult.handle_success_response(content, parse_content, class_name=cls_name)

