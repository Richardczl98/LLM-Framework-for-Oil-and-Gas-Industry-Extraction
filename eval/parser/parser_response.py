from __future__ import annotations

from typing import Optional, List
from dataclasses import dataclass

from .parser_result import ParseResult
import schema.variables as variables


@dataclass
class ParserResponse:
    """
        :param variables: The variables that the result may relate to.
                          If the `result.status` is 'success', only one variable in variables,
                          otherwise, all variables

    """
    field: str
    record: str
    section: str
    raw_text: str
    variable: Optional[variables.Variable]
    result: Optional[ParseResult]

    def __str__(self):
        return f"\nfield: {self.field}\nsection: {self.section}\nvariable: {self.variable.name}\nresult: {self.result}\n"


