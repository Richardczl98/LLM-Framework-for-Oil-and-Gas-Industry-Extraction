"""
Author: Alex <alex.hu@57blocks.com>
Date Created: 2023-10-19
Description: Mention parser class.
"""

from .parser import Parser
from typing import Any
from .parser_utils import handle_parser_error, convert_mentioned
from .parser_result import ParseResult, ParserSuccessResult, ParserErrorResult


class ParserMentioned(Parser):

    @handle_parser_error
    def parse(self, content: Any, key=None, unit=None) -> ParseResult:
        parse_content = super().init(content)
        err = int(not parse_content[0] in ("np.nan", "1"))
        cls_name = (type(self).__name__)

        if err:
            return ParserErrorResult.handle_err_response(content, parse_content,
                                                         class_name=cls_name)

        parse_content[0] = convert_mentioned(parse_content[0])
        return ParserSuccessResult.handle_success_response(
            content, parse_content, class_name=cls_name)


def remove_space(content: Any):
    content[0] = content[0].strip()
    space_num = content[0].count(' ')
    if space_num > 1:
        content[0] = content[0].replace(' ', space_num - 1)
    return content

