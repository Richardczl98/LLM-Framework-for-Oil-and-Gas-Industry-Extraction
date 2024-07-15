import logging
from typing import Optional, List
import pandas as pd

from config import YEAR_FOR_CALUCULATION
from schema.field import Field
from eval.xls_parser import ParseExcel, mark_duplicates
from eval.singleton import Singleton
from extractor.chat_llm import ask_llm_producing_year
from extractor.enum_fields import PaperTypeEnum


class FieldCollection(metaclass=Singleton):
    def __init__(self):
        self._field_list = []

    @property
    def field_list(self):
        return self._field_list

    def set_field_list_by_name(self,
                               field_names: List[str],
                               paper_text: str = '',
                               paper_type: str = ''):
        """
        Initialize fields with provided dict. This field may come from
        any source such LLM answer or user input.
        :param field_names: A list contain field names .
        :param paper_type: The type for reference paper,
                           used to check if need to ask producing years.
        For example: ['Hewitt Unit'  'okha','usinskoe'}.
        """

        if paper_type == PaperTypeEnum.FOCUSED_SURVEY_PAPER.value:
            field_dict = ask_llm_producing_year(paper_text, field_names)
        else:
            # we do not ask producing year for broad survey paper
            # as we assume broad survey paper touches lots of fields
            # without going too much details of various years
            # this is a balance between accuracy and resource consumed
            # as additional years multiply the time/money cost
            field_dict = {field: [] for field in field_names}

        fields, years = _flatten_field_dict(field_dict)
        fields_dp_name = mark_duplicates(fields)

        fields_tmp = []
        for fn, field_dn, year in zip(fields, fields_dp_name, years):
            field = Field(name=fn, display_name=field_dn, producing_year=year)
            fields_tmp.append(field)
        self._field_list = fields_tmp

    def set_field_list_from_gt(self, pe: ParseExcel):
        fields_tmp = []
        for d_name, field in zip(pe.fields_display, pe.fields):
            ground_truth = pe.parse_gt_value(d_name)

            field_age = ground_truth.get('Field age')
            producing_year = None if pd.isna(field_age) else int(YEAR_FOR_CALUCULATION - field_age)

            field = Field(name=field, display_name=d_name, producing_year=producing_year,
                          is_from_gt=True, duplicated=pe.is_duplicated(field))
            fields_tmp.append(field)

        self._field_list = fields_tmp

    def get_field(self, field_display: str) -> Optional[Field]:
        for field in self.field_list:
            if field_display == field.display_name:
                return field

    def __repr__(self):
        fields = []
        for field in self._field_list:
            fields.append(field.__repr__())

        return 'Fields: \n' + '\n'.join(fields)


def _flatten_field_dict(field_dict):

    fields = []
    field_years = []

    for field, years in field_dict.items():
        if years is None or len(years) == 0:
            fields.append(field)
            field_years.append(None)
        else:
            for year in years:
                fields.append(field)
                field_years.append(year)

    return fields, field_years


field_list = FieldCollection()
