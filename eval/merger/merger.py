from typing import Optional, Union, Literal
import pandas as pd

from eval.singleton import Singleton
from eval.parser.parser_result import SUCCESS, ERROR


class Merger(metaclass=Singleton):
    seperator = ' | '

    def merge(self, old: Optional[Union[str, float]], new: Optional[Union[str, float]]) -> Optional[Union[str, float]]:
        if pd.isna(old) or old == '':
            return new
        if pd.isna(new) or new == '':
            return old
        if old == new:
            return new

        return str(old) + self.seperator + str(new)

    @staticmethod
    def merge_status(old: str, new: str,) -> str:
        if old == ERROR:
            return old
        if new == ERROR:
            return new

        return new
