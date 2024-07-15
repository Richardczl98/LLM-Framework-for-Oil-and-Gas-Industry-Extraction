# -*- coding: utf-8 -*-
# Author: Anjing Wang
# Date: Oct-15-2023

"""
OPGEE Playground Command Line Interface (CLI) module.

This module provides a command line interface for play with OPGEE extraction.

Usage:
    python ask_llm.py -h
"""
import os
import sys
import argparse
import logging

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')

from lib import helper
from lib.my_logger import logger_config_instance, logger
from extractor.chat_llm import ask_extractor_question_from_ref
from script import show_tokens
from model import models, tokens
from extractor import chat_llm
from model.chat_openai import openai_client
from model.chat_anthropic import claude_client
from model.chat_mistral import mistral_client
from lib import file_op
# from extractor import extract_main

def get_pages(start_page, end_page, txt_folder):
    """
    Get pages between start and end
    need to consider page-10-11.txt
    """
    lst_pages = helper.get_sorted_filenames(txt_folder)
    lst_less_than_10 = []
    lst_larger_than_10 = []
    for page in lst_pages:
        page_no = helper.get_first_number(page)
        if page_no is None:
            continue
        if page_no < start_page:
            continue
        if page_no > end_page:
            continue
        if page_no >= 10:
            lst_larger_than_10.append(page)
        else:
            lst_less_than_10.append(page)

    return lst_less_than_10 + lst_larger_than_10

def test_get_pages():
    """
    test function
    """
    ret = get_pages(1, 2, '../result/spe-115712-ms/txt')
    print(ret)
    ret = combine_pages(ret, '../result/spe-115712-ms/txt')
    print(ret)

def combine_pages(lst_pages, txt_file_path):
    """
    Combine pages with proper page number indication
    """
    combined = ''
    for index, page in enumerate(lst_pages):
        content = helper.read_file(f'{txt_file_path}/{page}')
        page_no = page[:-4]
        page_no = page_no.replace('paper-', 'page ')
        if index == 0:
            str_beginning = f'This is the beginning of {page_no}\n'
        else:
            str_beginning = f'\nThis is the beginning of {page_no}\n'
        if index == len(lst_pages) - 1:
            str_end = f'\nThis is the end of {page_no}'
        else:
            str_end = f'\nThis is the end of {page_no}\n'

        combined += str_beginning + content + str_end

    return combined

def main():
    """
    A command line interface for the OPGEE LLM extractor.

    Parameters:
        None

    Returns:
        None
    """
    desp = 'Ask questions from a paper. Log is in /opgee/result/paper-name/time-model-playground/'
    parser = argparse.ArgumentParser(description=desp,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-p', '--paper',
                        type = str,
                        required = True,
                        help="The name of the paper. No extension and no path.")

    parser.add_argument('-m', '--model',
                    type = str,
                    choices = models.LST_MODEL_SUPPORTED,
                    default = 'gpt-4',
                    required = True,
                    help="llm model name")

    parser.add_argument('-rl', '--ref-loader',
                        type = str,
                        choices = ["sys", "page-manual"],
                        required = True,
                        help="sys: use sys default way to load all references and ask LLM multiple times.\n" +
                             "page-manual: mannually load references and ask LLM only one time.")

    parser.add_argument('-sp', '--start-page',
                        type = int,
                        help="Start page")

    parser.add_argument('-ep', '--end-page',
                        type = int,
                        help="End page")

    parser.add_argument('-s', '--sys_msg',
                        type = str,
                        default = 'sys_msg.txt',
                        help="The file contains prompt")

    parser.add_argument('-pt', '--prompt',
                        type = str,
                        default = 'prompt.txt',
                        help="your own prompt")

    parser.add_argument('-j', '--json_format',
                        action='store_true',
                        help="Output text with json format.")

    # Parse arguments
    args = parser.parse_args()
    ref_loader = args.ref_loader
    start_page = args.start_page
    end_page = args.end_page

    # make sure the relation between ref_loader and start/end_page
    if args.ref_loader == 'sys':
        if start_page is not None or \
           end_page is not None:
            print('--start-page and --end-page cannot be used with --ref-loader sys')
            return
    else:
        if start_page is None or \
           end_page is None:
            print('--start-page and --end-page must be used with --ref-loader page-manual')
            return

    txt_folder = show_tokens.verify_paper_prep(args.paper)
    if txt_folder == '':
        return
    output_file = f'{this_file_path}/playground/output.txt'

    role_txt = args.sys_msg
    if '/' not in role_txt:
        role_txt = f'{this_file_path}/playground/{role_txt}'
    if not os.path.exists(role_txt):
        logger.error('%s does not exist', args.sys_msg)
        return
    role = helper.read_file(role_txt)

    prompt_txt = args.prompt
    if '/' not in prompt_txt:
        prompt_txt = f'{this_file_path}/playground/{prompt_txt}'
    if not os.path.exists(prompt_txt):
        logger.error('%s does not exist', args.prompt)
        return
    prompt = helper.read_file(prompt_txt)

    # configure logger for this run
    paper_name = args.paper
    time_str = helper.get_time_str()
    result_folder = f'{this_file_path}/../result/{paper_name}/{time_str}-{args.model}-playground/'
    log_full_name = f'{result_folder}/{paper_name}.log'
    logger_config_instance.configure_logger(log_full_name,
                                            console_level=logging.INFO,
                                            console_format= '%(asctime)s-%(levelname)s %(message)s')

    if ref_loader == 'sys':
        rslts = chat_llm.ask_llm_txt_file(
            f'{txt_folder}/paper.txt',
            question=prompt,
            token_size=0,
            overlap_pages=0,
            overlap_token_size=100,
            splitter="token_size",
            model=args.model,
            json_format=args.json_format
        )

        full_resp = ''
        for resp in rslts:
            logger.info('\n' + resp)
            full_resp += (resp + '\n')

        file_op.write_to_file(full_resp, output_file)


        if models.is_model_openai(args.model):
            logger.info('cost saved for openai')
            openai_client.save_cost_to_file(result_folder + "/cost.txt")
        elif models.is_model_anthropic(args.model):
            logger.info('cost saved for claude')
            claude_client.save_cost_to_file(result_folder + "/cost.txt")
        elif models.is_model_mistral(args.model):
            logger.info('cost saved for mistral')
            mistral_client.save_cost_to_file(result_folder + "/cost.txt")
        else:
            logger.info('no cost is saved.')

        return

    # start to prepare the reference text
    if end_page is None:
        end_page = start_page

    if start_page < 1:
        print('Start page should be equal or larger than 1')
        return

    if end_page < start_page:
        print('End page should be larger than or equal to start page')
        return

    lst_pages = get_pages(start_page, end_page, txt_folder)
    ref_text = combine_pages(lst_pages, txt_folder)

    # the max possible user msg (ref + prompt)
    mtus = tokens.max_token_usr_msg(args.model, role)
    max_token_ref = mtus - tokens.count_tokens(args.model, prompt)
    token_num_ref = tokens.count_tokens(args.model, ref_text)
    token_num_role = tokens.count_tokens(args.model, role)
    token_num_prompt = tokens.count_tokens(args.model, prompt)
    if token_num_ref > max_token_ref:
        print('The token size exceeds the max.')
        print(f'token_num  role:{token_num_role} ref:{token_num_ref} prompt:{token_num_prompt}')
        return

    resp = ask_extractor_question_from_ref(model = args.model,
                                           ref = ref_text,
                                           question = prompt,
                                           sys_msg = role)
    logger.info('\n' + resp)
    file_op.write_to_file('\n' + resp, output_file)

    if models.is_model_openai(args.model):
        openai_client.save_cost_to_file(result_folder + "/cost.txt")
    elif models.is_model_anthropic(args.model):
        claude_client.save_cost_to_file(result_folder + "/cost.txt")
    elif models.is_model_mistral(args.model):
        logger.info('cost saved for mistral')
        mistral_client.save_cost_to_file(result_folder + "/cost.txt")

    return

if __name__ == "__main__":
    main()
    # test_get_pages()
