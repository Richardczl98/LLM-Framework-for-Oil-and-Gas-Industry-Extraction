"""
Author: Alex <alex.hu@57blocks.com>
Date Created: 2023-10-19
Description: Base parser class.
"""

from typing import Any
from .parser_utils import SPLIT_REF_CHAR
from abc import ABC, abstractmethod
from .parser_result import ParseResult
from lib.helper import split_at_first_char
from eval.singleton import Singleton


class Parser(ABC, metaclass=Singleton):

    def init(self, content: Any) -> Any:
        content = self.replace_mention(content)
        content = self.remove_qutoes(content)
        content = self.remove_commas(content)
        return content

    @abstractmethod
    def parse(self, llm_raw_response: Any, key=None, unit=None) -> ParseResult:
        pass

    def replace_mention(self, content: Any) -> Any:
        content = split_at_first_char(content , SPLIT_REF_CHAR)
        content[0] = content[0].replace("not_mentioned", "np.nan")
        content[0] = content[0].replace("Not_mentioned", "np.nan")
        content[0] = content[0].replace("Not mentioned", "np.nan")
        content[0] = content[0].replace("not mentioned", "np.nan")
        content[0] = content[0].replace("mentioned", "1")
        return content

    def remove_qutoes(self, content: Any) -> Any:
        content[0] = content[0].replace('"', '')
        content[0] = content[0].replace("'", '')
        return content

    def remove_commas(self , content: Any):
        content[0] = content[0].replace(',', '')
        return content
