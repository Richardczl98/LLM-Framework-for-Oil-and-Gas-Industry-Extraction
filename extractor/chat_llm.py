# -*- coding: utf-8 -*-
# Author: Alpha Xiang
# Date: Jul-2023
"""
Interact with the LLM to get answer
"""

import sys
import time
import json
from openai import OpenAIError
from retrying import retry
from typing import List

from model.splitter import split_txt_by_token_size, split_txt_by_page_num
import model.prompt_template as pt
from model import models, tokens, chat_webui, prompt_def
from model.chat_anthropic import claude_client
from model.chat_openai import openai_client
from model.chat_nlpcloud import nlp_cloud_client
from model.chat_google import google_ai_client
from model.chat_mistral import mistral_client
from model.models import MDL_GPT_4_T
from model.chat_mocked_model import mocked_llm_client
from lib import helper
from lib.my_logger import logger
from converter.pdf2txt import pdf_to_text, pdf_to_text_with_page
from converter.zip2txt import zip_to_text, zip_to_text_by_page_without_reference
import eval.parser.client as pc
import eval.merger.merge_by_block as merger
from eval.merger.fields_post_process import FieldsProcess
from schema.field import Field
from eval.parser.parser_producing_year import parse_producing_year


MAXIMUM_RETRY_NUMBER = 5


def is_openai_error(exception):
    # check whether an error is of type OpenAIError
    return isinstance(exception, OpenAIError)


def is_json_serialization_error(exception):
    return isinstance(exception, ValueError)


def preprocess_result(resp_txt:str):
    '''
    try to fix some format error for some model output
    but we do this for all models to be fair
    '''
    # mistal AI very likely escape _ as \\_
    # it adds a backslash before not\_mentioned
    # and in front ofmany other _
    resp_txt = resp_txt.replace('\\_', '_')
    return resp_txt


@retry(retry_on_exception=is_openai_error, stop_max_attempt_number=MAXIMUM_RETRY_NUMBER)
def _ask_llm_single_turn(model: str,
                        sys_msg: str,
                        prompt: str,
                        json_format: bool = False) -> str:
    """
    aggr to ask single turn question to LLM models
    """

    # the magic word is not in the begining as paper is in the front
    if prompt_def.PROMPT_MAGIC_RETURN_REST in prompt:
        index = prompt.index(prompt_def.PROMPT_MAGIC_RETURN_REST) + \
                len(prompt_def.PROMPT_MAGIC_RETURN_REST)
        return prompt[index:].strip()

    logger.info('NO MAGIC. Continue to ask LLM.')

    if models.is_model_openai(model):
        result = openai_client.chat_single_turn(prompt,
                                                model,
                                                sys_msg,
                                                json_format)

        # azure account has higher limit, do not need sleep
        # if not openai_client.is_use_azure:
        #     # TODO: remove once the key has higher limit
        #     time.sleep(50)
        if model == models.MDL_GPT_4_T:
            # azure has 80K rate limit per minute for gpt-4-turbo
            # we need to sleep and wait for the quote to recover
            # sleep for 60 seconds to make sure it's always in limit
            time.sleep(8)
        elif model == models.MDL_GPT_4_O:
            # saw retries in 4 seconds in log, so we sleep here just make sure
            time.sleep(4)
        elif model == models.MDL_GPT_35_16K:
            # azure has 120K rate limit per minute for gpt-3.5-turbo 16k 1106
            time.sleep(2)
    elif models.is_model_anthropic(model):
        result = claude_client.chat_single_turn(prompt,
                                                model,
                                                sys_msg)
    elif models.is_model_nlpcloud(model):
        result = nlp_cloud_client.chat_single_turn(prompt,
                                                   model,
                                                   sys_msg)
    elif models.is_model_google(model):
        result = google_ai_client.chat_single_turn(prompt,
                                                   model,
                                                   sys_msg)
    elif models.is_model_llama2(model):
        result = chat_webui.chat_single_turn(prompt)
    elif models.is_model_mistral(model):
        result = mistral_client.chat_single_turn(prompt,
                                                  model,
                                                  sys_msg)
    elif models.is_model_mocked(model):
        result = mocked_llm_client.chat_single_turn(prompt)
    else:
        logger.info("model: %s not supported", model)
        sys.exit()

    if not models.is_model_mocked(model):
        mocked_llm_client.update(prompt, result)

    # TODO: ideally, original result should be saved in raw
    # but preprocessed before parser
    result = preprocess_result(result)
    return result


def _ask_llm_question_from_ref(model: str,
                               sys_msg: str,
                               ref: str,
                               question: str,
                               json_format: bool = False) -> str:
    """
    cat ref with question
    """
    prompt = pt.pt_concatenate_question_ref(question, ref)
    if not prompt:
        return ''

    return _ask_llm_single_turn(model, sys_msg, prompt, json_format=json_format)


def ask_extractor_question_from_ref(model: str,
                                    ref: str,
                                    question: str,
                                    sys_msg: str = pt.SYS_MSG_EXTRACTOR,
                                    json_format: bool = False) -> str:
    """
    add extra function to differ purpose when interact with LLM
    """
    return _ask_llm_question_from_ref(model, sys_msg, ref, question, json_format=json_format)


def ask_formatter_instruct_and_ref(question: str,
                                   ref: str = '',
                                   model: str = 'gpt-4') -> str:
    """
    add extra function to differ purpose when interact with LLM
    """
    return _ask_llm_question_from_ref(model, pt.SYS_MSG_EXTRACTOR, ref, question)


def ask_assistant(question: str, model: str = 'gpt-4') -> str:
    """
    ask LLM for assistant
    """
    return _ask_llm_single_turn(model,
                               pt.SYS_MSG_ASSISTANT,
                               question)


def ask_llm_is_same_country(country_1: str, country_2: str, model: str = 'gpt-4') -> bool:
    """
    ask LLM if country 1 is country 2 or country_1 in country_2 or country 2 in country 1.
    """
    question = pt.pt_extract_country_and_compare_question(country_1, country_2)
    try:
        resp = _ask_llm_single_turn(model, pt.SYS_MSG_GEOGRAPHY_EXPERT, question)
    except Exception as err:
        logger.error(err)
        return False

    try:
        resp_json = json.loads(resp)
        rslt = resp_json.get('answer')
    except Exception as err:
        logger.error(err)
        return False

    if isinstance(rslt, bool):
        return rslt
    elif isinstance(rslt, str):
        if rslt.strip().lower() == 'true':
            return True
    return False


@retry(retry_on_exception = is_json_serialization_error,
       stop_max_attempt_number = MAXIMUM_RETRY_NUMBER)
def ask_llm_producing_year(paper_text: str,
                           field_names: List[str]):
    '''
    ask LLM for producing years and
    genearte field_dict with field name and producing years
    for further processing
    '''
    question = pt.pt_field_year_all(field_names)

    # ATTENTION: We always use gpt4-turbo to ask producing years
    # as we do not need to merge results if paper is too long
    # that needs to be splitted.
    result = ask_extractor_question_from_ref(model=MDL_GPT_4_T,
                                             ref=paper_text,
                                             question=question,
                                             json_format=True)
    logger.info("The producing year query output is:\n%s", result)

    try:
        rslt_json = json.loads(result)

    except Exception as err:
        logger.exception('Got exception when ask model producing year: ')
        logger.exception(err)
        return {field: [] for field in field_names}

    field_dict = parse_producing_year(rslt_json)

    # In case model cannot find producing year in paper result to miss fields.
    for field in field_names:
        if field.lower() not in [key.lower() for key in field_dict]:
            field_dict.update({field: []})

    return field_dict


# question should be composed within prompt template
def ask_llm_txt_file(txt_filename: str,
                     question: str,
                     token_size: int = 0,
                     overlap_pages: int = 0,
                     overlap_token_size: int = 100,
                     splitter="token_size",
                     model: str = 'gpt-4',
                     json_format: bool = False) -> list:
    """
    Split the text file into pieces,
    then ask the LLM for each piece
    Parameters:
        token_size = 0 means use token_num_max_block
    """
    outputs = []
    txt_paper = helper.read_file(txt_filename)
    if txt_paper == '':
        return ''

    token_num_paper = tokens.count_tokens(model, txt_paper)

    mtus = tokens.max_token_usr_msg(model)
    # max possible token size we can split the text
    token_num_max_block = mtus - tokens.count_tokens(model, question)

    # token size we used to split the text
    token_num_split_to = token_num_max_block
    # default token_size = 0 means use token_num_max_block
    if 0 < token_size <= token_num_max_block:
        token_num_split_to = token_size

    logger.info("token_num_paper: %s token_num_max_block %s token_num_split_to %s",
                token_num_paper,
                token_num_max_block,
                token_num_split_to)

    if splitter == "token_size":
        txt_splitted = split_txt_by_token_size(txt_paper,
                                               token_num_split_to,
                                               overlap_token_size,
                                               model=model)
        logger.info("The txt splitted into %s pieces", len(txt_splitted))
    else:
        txt_splitted = split_txt_by_page_num(txt_paper,
                                             overlap_pages,
                                             token_num_max_block,
                                             overlap_token_size,
                                             model=model)

    for index, ref in enumerate(txt_splitted):
        result = ask_extractor_question_from_ref(model, ref, question, json_format=json_format)
        logger.debug("The piece %s output is:\n%s", index, result)
        outputs.append(result)

    return outputs


def generate_block_files(txt_filename: str,
                         question: str,
                         token_size: int = 0,
                         overlap_pages: int = 0,
                         overlap_token_size: int = 100,
                         splitter="token_size",
                         model: str = 'gpt-4') -> list:
    """
    Split the text file into pieces,
    Parameters:
        token_size = 0 means use token_num_max_block, which result
        in the longest possible text block
    """
    txt_paper = helper.read_file(txt_filename)
    if txt_paper == '':
        return ''

    token_num_paper = tokens.count_tokens(model, txt_paper)

    mtus = tokens.max_token_usr_msg(model)
    # max possible number of tokens that we can split the paper(text)
    # into a block
    token_num_max_block = mtus - tokens.count_tokens(model, question)
    logger.debug("token_num_max_block %s mtus %s question_tokens %s question %s",
                 token_num_max_block,
                 mtus,
                 tokens.count_tokens(model, question),
                 question)

    # token size we used to split the text
    token_num_split_to = token_num_max_block

    # default token_size = 0 means use token_num_max_block
    if 0 < token_size <= token_num_max_block:
        token_num_split_to = token_size

    logger.info("token_num_paper: %s token_num_max_block %s token_num_split_to %s",
                token_num_paper,
                token_num_max_block,
                token_num_split_to)

    if splitter == "token_size":
        txt_splitted = split_txt_by_token_size(txt_paper,
                                               token_num_split_to,
                                               overlap_token_size,
                                               model=model)
    else:
        txt_splitted = split_txt_by_page_num(txt_paper,
                                             overlap_pages,
                                             token_num_max_block,
                                             overlap_token_size,
                                             model=model)
    logger.info("The txt splitted into %s pieces", len(txt_splitted))
    return txt_splitted


def ask_llm_methods_and_properties(txt_filename: str,
                                   eo_field: Field,
                                   model: str='gpt-4',
                                   splitter="token_size",
                                   token_size=0,
                                   grouped_by=pt.GroupedBy.SECTION) -> dict:
    """
    Extracts information from a TXT file for a single OIL fields.
    Returns:
        a list of a list containing LLM response result for a oil field
    """
    if grouped_by == pt.GroupedBy.SECTION:
        pt_method_and_property_funcs = pt.section_map
    elif grouped_by == pt.GroupedBy.INDIVIDUAL:
        pt_method_and_property_funcs = pt.pt_attribute_1to1_map

    # find the longest prompt, and use it to split the text
    max_prompt = ''
    max_prompt_token_len = 0
    for key_groupped, pt_prompt_func in pt_method_and_property_funcs.items():
        prompt = pt_prompt_func(eo_field.name)
        token_size = tokens.count_tokens(model, prompt)
        logger.debug('key_groupped %s prompt_len %s token_size %s',
                    key_groupped, len(prompt), token_size)
        if token_size > max_prompt_token_len:
            max_prompt_token_len = token_size
            max_prompt = prompt
    logger.debug('max_prompt_token_len: %s max_prompt: %s',
                 max_prompt_token_len, max_prompt)

    # use max_prompt as the question to split the text
    txt_splitted = generate_block_files(txt_filename=txt_filename,
                                        question=max_prompt,
                                        token_size=0,
                                        model=model,
                                        splitter=splitter)
    logger.debug("The txt splitted into %s pieces", len(txt_splitted))

    responses = []
    for index, ref in enumerate(txt_splitted):
        for key, pt_func in pt_method_and_property_funcs.items():
            # construct the question for every section
            question = pt_func(eo_field.name,
                               eo_field.get_producing_year())
            logger.debug('About to ask LLM for '
                         'oil/gas field: %s, '
                         'in splitted block: %s, '
                         'Section or attribute: %s, '
                         'prompt func: %s, '
                         'year:%s',
                          eo_field.display_name,
                          index,
                          key,
                          pt_func.__name__,
                          eo_field.get_producing_year())
            result = ask_extractor_question_from_ref(model, ref, question)
            logger.debug("Got LLM response for block %s:\n%s", index, result)
            if grouped_by == pt.GroupedBy.SECTION:
                parser = pc.ParserClient(model=model, field_name=eo_field.name,
                                         reference=ref, section=key)
            elif grouped_by == pt.GroupedBy.INDIVIDUAL:
                # make a list that only contains the key, which is the variable name
                var_lst = [key]
                parser = pc.ParserClient(model=model, field_name=eo_field.name,
                                         reference=ref, variables=var_lst)
            parser.parse(result)
            responses += parser.get_responses()
            logger.debug('After ask LLM - sec: %s,template: %s, field: %s, year:%s, block: %s',
                            key,
                            pt_func.__name__,
                            eo_field.display_name,
                            eo_field.get_producing_year(),
                            index)
        FieldsProcess().fields_post_process(responses)

    results = merger.merge_by_block(responses)
    logger.debug(f'Finish to ask llm in {txt_filename} for {eo_field.display_name}, results: \n{results}')

    return results


# zip files are extracted by page
# TODU Ask questions by page
def llm_run_from_pages(pages: list,
                       oid_field_name: str,
                       pt_method_or_properties,
                       max_token_size: int = 7500,
                       overlap_page: int = 0,
                       overlap_token_size: int = 100,
                       model: str = 'Llama-2-70B-chat-GPTQ') -> list:
    docs = split_pages(pages,
                       overlap_pages=overlap_page,
                       overlap_token_size=overlap_token_size,
                       max_token_size=max_token_size,
                       model=model)
    prompt_templates = pt_method_or_properties(oid_field_name)
    outputs = []

    for index, doc in enumerate(docs):
        if isinstance(prompt_templates, str):
            usr_msg = doc + "\n" + prompt_templates
            result = llm_run_single_prompt_template(model, usr_msg)
            outputs.append(result)
        elif isinstance(prompt_templates, list):
            for prompt_template in prompt_templates:
                usr_msg = doc + "\n" + prompt_template
                result = llm_run_single_prompt_template(model, usr_msg)
                outputs.append(result)
        else:
            raise ValueError(prompt_templates)
    return outputs


def llm_run_from_zip(zip_file: str,
                     oid_field_name: str,
                     pt_method_or_properties,
                     max_token_size: int = 7500,
                     overlap_size: int = 100,
                     overlap_page: int = 0,
                     overlap_token_size: int = 100,
                     type: str = "text",
                     mode: str = "csv",
                     model: str = 'Llama-2-70B-chat-GPTQ', ) -> list:
    if type == "page":
        whole_paper, pages_dict = zip_to_text_by_page_without_reference(zip_file, mode=mode)
        pages_txt = pages_dict.values()
        outputs = llm_run_from_pages(pages_txt,
                                     oid_field_name,
                                     pt_method_or_properties,
                                     max_token_size=max_token_size,
                                     overlap_page=overlap_page,
                                     overlap_token_size=overlap_size,
                                     model=model)

    else:
        whole_paper = zip_to_text(zip_file, mode=mode)
        outputs = llm_run_from_text(whole_paper,
                                    oid_field_name,
                                    pt_method_or_properties,
                                    max_token_size=max_token_size,
                                    overlap_token_size=overlap_token_size,
                                    model=model)
    return outputs


def llm_run_from_pdf(pdf,
                     oid_field_name: str,
                     pt_method_or_properties,
                     max_token_size=7500,
                     overlap_token_size=100,
                     overlap_page=1,
                     type="page",
                     model="llama2"):
    # load data
    if type == "page":
        whloe_text, pages_dict = pdf_to_text_with_page(pdf)
        pages_txt = pages_dict.values()
        outputs = llm_run_from_pages(pages_txt,
                                     oid_field_name,
                                     pt_method_or_properties,
                                     max_token_size=max_token_size,
                                     overlap_page=overlap_page,
                                     overlap_token_size=overlap_token_size,
                                     model=model)
    else:
        whloe_text = pdf_to_text(pdf)
        outputs = llm_run_from_text(whloe_text,
                                    oid_field_name,
                                    pt_method_or_properties,
                                    max_token_size=max_token_size,
                                    overlap_token_size=overlap_token_size,
                                    model=model)
    return outputs


if __name__ == '__main__':
    # test_llm_run_from_text()
    # test_llm_run_from_pages()
    # test_llm_run_from_zip()
    # print(ask_llm_question_of_ref('who is feifei?',
    #                               'feifei is an artist.'))
    pass