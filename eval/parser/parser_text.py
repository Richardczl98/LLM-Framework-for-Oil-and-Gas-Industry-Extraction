"""
Author: Alex <alex.hu@57blocks.com>
Date Created: 2023-10-19
Description: Text parser class.
"""

from .parser_utils import SPLIT_REF_CHAR
from typing import Any
from .parser import Parser
from lib.helper import split_at_first_char
from .parser_result import ParseResult, ParserSuccessResult
import numpy as np

class ParserText(Parser):

    def parse(self, content: Any, key=None, unit=None) -> ParseResult:
        parse_content = split_at_first_char(content, SPLIT_REF_CHAR)
        parse_content[0] = np.nan if (
                    parse_content[0].lower() == "not_mentioned" or parse_content[0].lower() == "not mentioned") else \
        parse_content[0]
        cls_name = (type(self).__name__)
        return ParserSuccessResult.handle_success_response(content, parse_content, class_name=cls_name)
