import os
import sys
from typing import Optional
from dataclasses import dataclass, field
from collections import OrderedDict
import pandas as pd


this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')


@dataclass
class Field:
    name: str           # Field name may be duplicated
    display_name: str   # unique display name for each field
    producing_year: int = None
    is_from_gt: bool = False
    duplicated: bool = False

    def get_producing_year(self) -> Optional[int]:
        """
        Get the year of field age from ground truth. Current only consider duplicated fields.

        Param: None

        Returns: If "Field age" have a value in ground truth, return the calculated year,
                 otherwise return None.
        """
        # same_year_fields = ['Marmul Field, Haima West Reservoir', 'Niger Delta', 'North Dome', 'North Field', 'south belridge', 'Tiguino']
        if self.is_from_gt:
            return self.producing_year if self.duplicated else None
        else:
            return self.producing_year

    def __hash__(self):
        return hash(self.display_name)

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.display_name == other.display_name
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f'Field(name={self.name}, display_name={self.display_name}, '
            f'producing year={self.producing_year}, is_from_gt={self.is_from_gt}, duplicated_in_gt={self.duplicated}'
        )
