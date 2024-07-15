import os
from pathlib import Path
from collections import OrderedDict
from typing import Tuple
import json

from config import UNKNOWN_TEXT
from eval.xls_parser import ParseExcel, ParseEvaluationExcel
from eval.parser.client import ParserClient
import eval.merger.merge_by_block as merger
from eval.merger.fields_post_process import FieldsProcess
from converter.dict2xls import convert_dict_to_xls
from eval import eval_main
from lib.helper import find_ground_truth_files
from lib.my_logger import logger


def parse_path(raw_file_path: str, destination: str) -> Tuple[str, str, str]:
    if not Path(raw_file_path).exists():
        raise FileNotFoundError(f"{raw_file_path} does not exists")

    paper_name = Path(raw_file_path).parts[-3]
    parent_dir_name = Path(raw_file_path).parts[-2]
    gt_path = find_ground_truth_files(paper_name)
    result_middle_path = os.path.join(paper_name, parent_dir_name)
    dest_path = os.path.join(destination, result_middle_path)
    log_full_name = f'{dest_path}/{paper_name}.log'

    return gt_path, dest_path, log_full_name


def extract_history(raw_file_path: str, dest_path: str, gt_path: str, model: str = 'gpt-4', success_only: bool = False):
    """
    Main process of extract history extract_raw.xlsx files.
        1. Handle related file path.
        2. Parse extract_raw.xlsx.
        3. write parsed results.
        4. Evaluate parsed results.

    :param raw_file_path: path of extract_raw.xlsx file
    :param dest_path: output directory to store excels files with parsed data
    :param gt_path: path of ground truth file
    :param model: the model generate raw text
    :param success_only: Only display and evaluate successfully parsed values in result excels.

    :return: dictionary contain parsed values
    """
    history_rslts = parse_history(raw_file_path, model)
    pe = ParseExcel(gt_path)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    with open(os.path.join(dest_path, 'extract.json'), 'w') as fp:
        json.dump({"prediction": history_rslts, "ground-truth": pe.to_dict()}, fp)

    convert_dict_to_xls(dest_path, history_rslts, ground_truth=pe, success_only=success_only)
    logger.info("Finish to save all history field results to %s", dest_path)

    eval_main.evaluate(history_rslts, pe, dest_path, success_only=success_only)


def parse_history(extract_raw_path: str, model: str = 'gpt-4') -> OrderedDict:

    """
    Parse and merge values from extract_raw excel.

    :param extract_raw_path: path of extract_raw.xlsx file
    :param model: the model generate raw text

    :return: dictionary contain parsed values
        dict={
            "fields":[oil_field_1,oil_field_2,......,oil_field_n],
            “oil_field_1”:{
                variable_1: [value_1, unit_1, raw_text_1, record_1],
                variable_2: [value_2, unit_2, raw_text_2, record_2],
                ......
                variable_n:[value_n, unit_n, raw_text_n, record_n]
            },
            ...
        }
    """
    extract_raw = ParseEvaluationExcel(extract_raw_path)

    rslts = OrderedDict()
    for (col, blocks), field in zip(extract_raw.blocks.items(), extract_raw.fields):
        resp = []
        for block in blocks.values():
            parser_client = ParserClient(model=model, field_name=field, variables=extract_raw.variables)
            for variable, raw_value in block.items():
                if variable == 'Field name' or raw_value == UNKNOWN_TEXT:
                    continue
                logger.info(f"Parse Value: {variable}: {raw_value}")
                parser_client.parse_value(raw_record='', key=variable, raw_value_text=raw_value)
            parser_client.complete_missing_responses()
            # parser_client.show_responses()
            # parser_client.show_failed_responses()
            resp += parser_client.get_responses()

            FieldsProcess().fields_post_process(resp)
        merged_rslts = merger.merge_by_block(resp)

        rslts.update({col: merged_rslts})
    logger.info(f"Parser Responses: {rslts}")
    return rslts
