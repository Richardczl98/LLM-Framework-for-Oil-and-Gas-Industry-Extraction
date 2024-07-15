# -*- coding: utf-8 -*-
# Author: Anjing Wang
# Date: Oct-05-2023

"""
OPGEE Command Line Interface (CLI) module.

This module provides a command line interface for the OPGEE program,
allowing users to input the title of a paper and, optionally,
a path to an xls file containing ground truth.

Usage:
    python opgee_cli.py -p "Title of the paper" [-g /path/to/groundtruth.xls]
"""
import os

import argparse
import time
from extractor.enum_fields import EnumFields
import json

from lib import helper, file_op
from lib.my_logger import logger_config_instance, logger
import model.prompt_template as pt
from model.chat_openai import openai_client
from model.chat_anthropic import claude_client
from model.chat_mistral import mistral_client
from model.chat_mocked_model import mocked_llm_client
from model import models
from extractor import extract_main
from eval import eval_main, xls_parser
from converter.dict2xls import convert_dict_to_xls
from schema.fields import field_list


this_file_path = os.path.dirname(os.path.realpath(__file__))


def main():
    """
    A command line interface for the OPGEE LLM extractor.

    Parameters:
        None

    Returns:
        None
    """
    desp = 'OPGEE LLM extractor CLI. Result is in /opgee/result/paper-name/time-model/'
    parser = argparse.ArgumentParser(description=desp)

    # Paper's title
    parser.add_argument('-p', '--paper',
                        type=str,
                        required=True,
                        help="Path of the paper (pdf, txt or zip) to be processed")

    parser.add_argument('-g', '--groundtruth',
                        type=str,
                        help="Path to the xls file containing ground truth")

    # how attribute propmts are grouped together
    # For example, gpt-4 can handle a long questions grouped by section
    # gpt-3.5-turbo can only handle a short question
    parser.add_argument('--grouped_by',
                        type=str,
                        choices=["section", "individual"],
                        required=True,
                        default="section",
                        help="prompt grouped by section or individual.")

    parser.add_argument('-t', '--token_size',
                        default=0,
                        type=int,
                        help="Split the text into pieces by token_size."
                             "The defaut value 0 means the maximum number of tokens for the model")

    parser.add_argument('-sp', '--splitter',
                        type=str,
                        default="token_size",
                        choices=["token_size", "page_num"],
                        help="split text by token_size or page_num.")

    parser.add_argument('-m', '--model',
                        type=str,
                        choices=models.LST_MODEL_SUPPORTED,
                        required=True,
                        help="llm model name")

    parser.add_argument("--max_field",
                        type = int,
                        default = 0,
                        help = "Maxium number of oil fields to extract.")

    parser.add_argument("-d", "--deep_run",
                        action='store_true',
                        help=("For deep run, field name and year would be from model, "
                             "otherwise they are from ground truth file."))

    parser.add_argument("-so", '--success_only',
                        action='store_true',
                        default=False,
                        help=("Only display and evaluate "
                              "successfully parsed values in result excels."))

    time_start = time.time()
    # Parse arguments
    args = parser.parse_args()

    # validate arguments
    if not os.path.exists(args.paper):
        logger.error('%s does not exist', args.paper)
        return

    if args.groundtruth and not os.path.exists(args.groundtruth):
        logger.error('%s does not exist', args.groundtruth)
        return

    # configure logger for this run
    paper_name = helper.get_paper_name(args.paper)
    time_str = helper.get_time_str()
    result_folder = f'{this_file_path}/result/{paper_name}/{time_str}-{args.model}-{args.grouped_by}/'
    log_full_name = f'{result_folder}/{paper_name}.log'
    logger_config_instance.configure_logger(log_full_name)

    # covert prompt template grouped by
    if args.grouped_by == "section":
        args.grouped_by = pt.GroupedBy.SECTION
    elif args.grouped_by == "individual":
        args.grouped_by = pt.GroupedBy.INDIVIDUAL
    else:
        print(f"Unsupported prompt style: {args.grouped_by}")
        return

    # Access the arguments using args.argument_name
    # (e.g., args.paper, args.eval, args.groundtruth)
    pe = None
    fields = []
    logger.info("Processing paper: %s args.paper")
    if not args.groundtruth or args.deep_run:
        logger.info("Start deep run - query field names and years from paper: ")
        fields_enum = EnumFields()
        fields_enum.set_paper(args.paper)
        lst_paper_fields = fields_enum.get_field_list()
        if len(lst_paper_fields) == 0:
            # spe-93031-ms: example that no fields can be extracted
            txt_file_no_fields = f'{result_folder}/no_fields.txt'
            file_op.write_to_file(content = fields_enum.fields_text,
                                  file_path = txt_file_no_fields)
            logger.info("No fields enumerated from the paper, opgee_cli exit.")
            return
        field_list.set_field_list_by_name(lst_paper_fields,
                                          fields_enum.paper_text,
                                          fields_enum.identify_type())
    else:
        # at this point, groundtruth is not None
        logger.info("Start shallow run - "
                    "read field names and years from ground truth: %s",
                    args.groundtruth)
        if not os.path.exists(args.groundtruth):
            logger.error('%s does not exist', args.groundtruth)
            return

        pe = xls_parser.ParseExcel(args.groundtruth)
        field_list.set_field_list_from_gt(pe)

    fields = field_list.field_list
    if len(fields) == 0:
        # should not run to here, because we should have at least one field
        logger.error("No fields extracted, opgee_cli exit.")
        return
    logger.info("Extracted %d fields: %s", len(fields), fields)

    # limit the number of fields if max_field is set
    # when we need to have a limited run to save time and cost
    if args.max_field > 0:
        fields = fields[:args.max_field]

    logger.info("Start to extract fields from %s for the above fields",
                args.paper)
    if args.paper.endswith(".pdf"):
        rslts = extract_main.extract_from_pdf(args.paper, fields, args.grouped_by,
                                              args.model, args.splitter,
                                              args.token_size,
                                              save_folder=result_folder)
    elif args.paper.endswith(".zip"):
        rslts = extract_main.extract_from_zip(args.paper, fields, args.grouped_by,
                                              args.model, args.splitter,
                                              args.token_size,
                                              save_folder=result_folder)
    elif args.paper.endswith(".txt"):
        rslts = extract_main.extract_from_txt(args.paper, fields, args.grouped_by,
                                              args.model, args.splitter,
                                              args.token_size,
                                              save_folder=result_folder)
    else:
        print(f"Unsupported file type: {args.paper}")
        return

    with open(os.path.join(result_folder, 'extract.json'), 'w') as fp:
        json.dump({"prediction": rslts, "ground-truth": pe.to_dict()}, fp)

    convert_dict_to_xls(result_folder, rslts,
                        ground_truth=pe,
                        success_only=args.success_only)
    logger.info("Finish to save all results to %s", result_folder)

    dict_stats = {}
    if models.is_model_openai(args.model):
        dict_stats = openai_client.get_stats()
    elif models.is_model_anthropic(args.model):
        dict_stats = claude_client.get_stats()
    elif models.is_model_mistral(args.model):
        dict_stats = mistral_client.get_stats()

    if args.groundtruth:
        eval_main.evaluate(rslts, pe, result_folder,
                           success_only=args.success_only,
                           deep_run=args.deep_run)

    mocked_llm_client.dump(result_folder + 'history_llm_answers.json')

    time_end = time.time()
    dict_stats['time'] = time_end - time_start
    file_op.save_dict_to_json(dict_stats, result_folder + "stats.json")

    return


if __name__ == "__main__":
    main()
