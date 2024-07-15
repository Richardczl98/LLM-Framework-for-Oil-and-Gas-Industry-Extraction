"""
Author: Alex <alex.hu@57blocks.com>
Date Created: 2023-10-19
Description: Category parser class.
"""

from .parser_numeric import ParserNumeric
from typing import Any
from .parser_utils import handle_parser_error
from .parser_result import ParseResult

class ParserCategory(ParserNumeric):

    @handle_parser_error
    def parse(self, content:Any, key=None, unit=None) -> ParseResult:
        return super().parse(content, key, unit)

