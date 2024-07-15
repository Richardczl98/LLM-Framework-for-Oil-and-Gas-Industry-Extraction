"""
Author: Alex <alex.hu@57blocks.com>
Date Created: 2023-10-19
Description: Result wrapper class.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional, Dict, Callable

import numpy as np

from lib.my_logger import logger

from eval.exception import RESULT_FORMAT_ERROR, ParserException

SUCCESS = "success"
ERROR = "error"


@dataclass
class ParserData(Dict):
    value: str | float | np.nan = None
    ref: str = None
    unit: str = None
    status: Literal[SUCCESS, ERROR] = SUCCESS

    def __str__(self) -> str:
        return f'{self.__dict__}'


@dataclass
class ParserSuccessResult:
    data: ParserData
    feedback: Optional[Callable] = None
    status: Literal[SUCCESS] = SUCCESS
    error: Optional[ParserException] = None

    @classmethod
    def handle_success_response(self, *args, error_stack: str = "", unit="",
                                class_name: str = "") -> ParserSuccessResult:
        err = SUCCESS
        content = args[0]
        parse_content = args[1]
        logger.debug(f"Success parser {content}")
        data = ParserData(parse_content[0], parse_content[1], unit, status=err)
        return ParserSuccessResult(data=data)

    def __str__(self) -> str:
        return f"Parse succeeded and returned: `{self.data}`"


@dataclass
class ParserErrorResult:
    data: ParserData
    feedback: Optional[Callable] = None
    error: Optional[ParserException] = None
    status: Literal[ERROR] = ERROR

    @classmethod
    def handle_err_response(self, *args, code=RESULT_FORMAT_ERROR, error_stack: str = "", unit="",
                            class_name: str = "") -> ParserErrorResult:
        err = ERROR
        content = args[0]
        parse_content = args[1]
        logger.debug(f"Could not parser {content}:{str(error_stack)}\n")
        data = ParserData(parse_content[0], parse_content[1], unit, status=err)
        return ParserErrorResult(
            data=data,
            error=ParserException(code, {"exception": str(error_stack), "content": content}, cls_name=class_name)
        )

    def __str__(self) -> str:
        return f"Parse failed: `{self.data}` , errorStack: `{self.error}` "


ParseResult = ParserSuccessResult | ParserErrorResult
