import os.path

import pandas as pd
from collections import OrderedDict
from typing import List, Optional
from pathlib import Path
import numpy as np

from config import SPLIT_BLOCK_CHAR, UNKNOWN_TEXT, AGGREGATE_COLUMN_NAME_SPLITTER, ROOT_DIR
from eval.parser.parser_utils import SPLIT_REF_CHAR
from schema.variables import get_all_variable, get_units_all, get_variable
from lib.my_logger import logger


SKIP_ROWS = 4
SKIP_COLUMNS = 7


class ParseExcelBase:

    def to_dataframe(self) -> pd.DataFrame:
        raise NotImplementedError

    def to_excel(self, path: str, create: bool = False, sheet='Sheet1'):
        if not (parent_dir := Path(path).parent).exists():
            os.makedirs(str(parent_dir))
        if create:
            mode = 'w'
        else:
            mode = 'a'

        df = self.to_dataframe()
        df.insert(0, 'Unit', np.array(get_units_all()))

        with pd.ExcelWriter(path, engine='openpyxl', mode=mode) as writer:
            df.to_excel(writer, sheet_name=sheet, na_rep='')


class ParseExcel(ParseExcelBase):
    '''
    parse ground truth excel
    '''
    def __init__(self, excel_file: Optional[str | Path] = None):
        self.file_path = excel_file
        logger.debug('ground truth file: %s', self.file_path)
        self.data: pd.DataFrame
        if excel_file:
            self.data = pd.read_excel(
                self.file_path,
                skiprows=SKIP_ROWS
            )
        else:
            self.data = pd.DataFrame()
        self.fields: List[str] = self._parse_oil_fields() if excel_file else []
        self.fields_display: List[str] = mark_duplicates(self.fields)
        self.sections: List[str] = self._parse_section() if excel_file else []
        self.columns = self.data.columns.tolist()[SKIP_COLUMNS: SKIP_COLUMNS + len(self.fields_display)] if excel_file else []

    def parse_gt_value(self, field_dn: str) -> OrderedDict:
        ground_truth = OrderedDict()

        if field_dn in self.fields_display:
            variables = get_all_variable(only_gt=True)
            column_in_gt = self.columns[self.fields_display.index(field_dn)]
            for var in variables:
                row_id = get_shifted_row(var.gt_row)
                ground_truth.update({var.name: self.data.at[row_id, column_in_gt]})
        return ground_truth

    def _parse_section(self) -> List[str]:
        section_idx = [7, 19, 33, 44, 69, 80]
        section_col = 'Unnamed: 0'

        sections = []
        for row_id in section_idx:
            shifted_row = get_shifted_row(row_id)
            sections.append(self.data.at[shifted_row, section_col])

        return sections

    def _parse_oil_fields(self):
        field_var = get_variable(var_names=['Field name'])[0]
        start_col_name = 'Unit'
        row_id = get_shifted_row(field_var.gt_row)
        fields = self.data.loc[row_id, start_col_name:].dropna().drop(index='Default').values

        return [f.strip() for f in fields]

    def is_duplicated(self, field_name: str):
        tmp = []
        for fn in self.fields:
            if fn == field_name:
                tmp.append(fn)
        return True if len(tmp) > 1 else False

    def to_dict(self, into: type[dict] = OrderedDict) -> dict | OrderedDict:
        return self.to_dataframe().to_dict(into=into)

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame()
        for field_dn in self.fields_display:
            field_dt = self.parse_gt_value(field_dn)
            df[field_dn] = pd.Series(field_dt)
        # df.insert(0, 'Unit', np.array(get_units_all()))

        return df

    def __repr__(self):
        return str(self.__class__) + ': \n' + '\n'.join([field + ': ' + str(self.__dict__[field]) for field in self.__dict__])


class ParseEvaluationExcel(ParseExcelBase):
    def __init__(self, excel_file: str, sheet: str = 'Sheet1'):
        self.data = pd.read_excel(excel_file, sheet_name=sheet)
        self.excel_file = excel_file

        self.data.rename(columns={'Unnamed: 0': 'variables'}, inplace=True)
        self.variables = self.data['variables'].tolist()

        if 'units' in self.data.columns:
            self.data.rename(columns={'units': 'unit'}, inplace=True)
        self.units = self.data['unit'].to_dict(into=OrderedDict)
        self.data.drop(columns='unit', inplace=True)
        self.data.set_index('variables', drop=True, inplace=True)
        self.columns = list(self.data.columns)
        self.fields = self.data.loc['Field name'].tolist()

        self.block_size = self._get_block_number()
        self.blocks = self._extract_blocks()
        self.raw_properties = self._make_raw_properties()

    def _get_block_number(self):
        print(self.excel_file)
        max_num = 1
        for col in self.columns:
            new_max = self.data[col].apply(lambda x: len(x.split(SPLIT_BLOCK_CHAR))).max()
            if new_max > max_num:
                max_num = new_max

        return max_num

    def _extract_blocks(self) -> OrderedDict:
        blocks = OrderedDict()
        for col, field in zip(self.columns, self.fields):
            data = self.data[[col]].copy()
            for b_id in range(self.block_size):
                data[f'block_{b_id}'] = data[col].apply(lambda x: _split_block(x, self.block_size)[b_id])
            # print(data.to_dict())
            data.drop(labels=col, inplace=True, axis=1)
            blocks.update({col: data.to_dict(into=OrderedDict)})
        return blocks

    def _make_raw_properties(self):
        raw_text_fields = {}
        for field, blocks in self.blocks.items():
            block_text = {}
            for block, variables in blocks.items():
                properties = ''
                for key, value in variables.items():
                    if value == UNKNOWN_TEXT:
                        continue

                    properties += '{' + key + ':' + value + '}\n'
                block_text.update({block: properties})
            raw_text_fields.update({field: block_text})

        return raw_text_fields


class ParseAggregatedExcel(ParseExcelBase):
    spliter = AGGREGATE_COLUMN_NAME_SPLITTER
    paper_columns_start = 2

    def __init__(self, excel_file: str, sheet: str = 'ref'):
        if not os.path.isabs(excel_file):
            excel_file = ROOT_DIR / excel_file
        self.data = pd.read_excel(excel_file, sheet_name=sheet)
        self.data.rename(columns={'Unnamed: 0': 'variables'}, inplace=True)
        self.data.set_index('variables', inplace=True)
        self.gt_columns = self._parse_gt_columns()
        self.pred_columns = self._parse_pred_columns()
        self.papers = self._parse_papers()

    def _parse_papers(self):
        columns = [col.split(self.spliter)[0] for col in self.data.columns[self.paper_columns_start:]]
        return sorted(set(columns))

    def _parse_gt_columns(self):
        columns = [col for col in self.data.columns[self.paper_columns_start:] if 'GT' in col]
        return columns

    def _parse_pred_columns(self):
        columns = [col for col in self.data.columns[self.paper_columns_start:] if 'GT' not in col]
        return columns

    def to_dict(self, papers: List[str] = None, fields: List[str] = None) -> OrderedDict:
        pred_data = OrderedDict()

        if not papers:
            for col in self.pred_columns:
                paper, field_name = col.split(self.spliter)
                paper_dt = pred_data.get(paper, OrderedDict())
                paper_dt[field_name] = self.data[col].to_dict(into=OrderedDict)
                pred_data[paper] = paper_dt

            return pred_data
        else:
            for col in self.pred_columns:
                if len(col_parts := col.split(self.spliter)) == 2:
                    paper = col_parts[0]
                    if paper in papers:
                        field_display_name = col_parts[1]

                        if fields and field_display_name in fields:
                            pred_data[paper] = pred_data.get(paper, OrderedDict())
                            pred_data[paper][field_display_name] = self.data[col].to_dict(into=OrderedDict)

            return pred_data


def _split_block(text: str, block_max: int):
    """
    Split raw text from extract_raw by block.
    :param text: the string text need to be split
    :param block_max: the max number of blocks included in text.
    """

    blocks = text.strip().split(SPLIT_BLOCK_CHAR)
    blocks.reverse()
    original_blocks = blocks.copy()
    for _ in range(block_max - len(blocks)):
        original_blocks.append(blocks[-1])
    original_blocks.reverse()

    return original_blocks


def get_shifted_row(raw_id: int) -> int:
    # The first -1 is because excel index start from 1, but DataFrame statr from 0.
    # The second -1 is because the 5th row in ground truth is used as the column in its DataFrame.
    return raw_id - SKIP_ROWS - 1 - 1


def _get_value(text: str) -> str:

    blocks_raw = text.split(SPLIT_BLOCK_CHAR)
    blocks = [block.strip().split(SPLIT_REF_CHAR) for block in blocks_raw]
    values = [block[0] for block in blocks]

    return SPLIT_BLOCK_CHAR.join(values)


def mark_duplicates(fields: List[str]):
    seen = {}
    result = []
    for field in fields:
        if field not in seen:
            seen[field] = 0
            result.append(field)
        else:
            seen[field] += 1
            result.append(f"{field}_{seen[field]}")
    return result
