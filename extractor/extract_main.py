# -*- coding: utf-8 -*-
# Author: Anjing Wang
# Date: Oct-06-2023

""" The main entry for extractor """

import os
import sys
from collections import OrderedDict

from converter.zip2txt import zip_to_text_with_page
from converter.pdf2zip import pdf_text_tabel_to_zip
from extractor import chat_llm
from lib.my_logger import logger
from lib import helper
import model.prompt_template as pt

def extract_from_txt(txt_file_name: str,
                     oil_fields: list,
                     grouped_by: pt.GroupedBy,
                     model: str,
                     splitter="token_size",
                     token_size = 0,
                     save_folder: str = None) -> OrderedDict:
    """
    Extracts information from a TXT file based on the given parameters.

    Parameters:
        txt_file_name (str): The name of the TXT file.
        oil_field_names (list): A list of oil field names.
        grouped_by (pt.GroupedBy): How questions are grouped together
        model (str, optional): The model to use.
        save_folder (str, optional): The folder to save the results. Defaults to "result".

    Returns:
        None
    """
    # it has to be a txt file
    if not txt_file_name.endswith(".txt"):
        return False
    if not os.path.exists(txt_file_name):
        logger.critical('%s does not exist', txt_file_name)
        sys.exit()

    all_field_rslts = OrderedDict()

    for field in oil_fields:
        logger.debug("Start to ask field:%s year: %s",
                     field.display_name,
                     field.get_producing_year())

        responses = chat_llm.ask_llm_methods_and_properties(
                txt_file_name,
                field,
                model=model,
                splitter=splitter,
                token_size=token_size,
                grouped_by=grouped_by
            )
        all_field_rslts.update({field.display_name: responses})

        logger.debug("Finish to ask field:%s year: %s", field.display_name, field.get_producing_year())
    logger.debug('Finish analyze for paper %s', txt_file_name)

    return all_field_rslts


def save_txt_from_zip(zip_file_name: str,
                      rslt_folder: str) -> bool:
    """
    convert the zip file to seperate page
    """
    # it has to be a zip file
    if not zip_file_name.endswith(".zip"):
        return False

    # validate zip file exists
    if not os.path.exists(zip_file_name):
        logger.error('%s does not exist', zip_file_name)
        return False

    save_extract_txt_folder = f"{rslt_folder}/txt/"
    if not os.path.exists(save_extract_txt_folder):
        os.makedirs(save_extract_txt_folder)

    zip_to_text_with_page(zip_file_name,
                          save_to_disk = True,
                          save_folder = save_extract_txt_folder)

    return True


def extract_from_zip(zip_file_name: str,
                     oil_field_names: list,
                     grouped_by: pt.GroupedBy,
                     model: str,
                     splitter="token_size",
                     token_size=None,
                     save_folder: str = None) -> OrderedDict:
    """
    save txt first, then extract
    """
    if save_txt_from_zip(zip_file_name, save_folder) is False:
        return False

    save_extract_txt_folder = f"{save_folder}/txt/"
    txt_file_abs_path = save_extract_txt_folder + "/paper.txt"

    all_field_rslts = extract_from_txt(txt_file_abs_path, oil_field_names,
                                       grouped_by, model=model,
                                       token_size=token_size, splitter=splitter,
                                       save_folder=save_folder)
    return all_field_rslts


def extract_from_pdf(pdf_file_name: str,
                     oil_field_names: list,
                     grouped_by: pt.GroupedBy,
                     model,
                     splitter="token_size",
                     token_size=None,
                     save_folder: str = None) -> OrderedDict:
    """
    save_folder: always /opgee/result/paper-name/time-model
    """
    # it has to be a pdf file
    if not pdf_file_name.endswith(".pdf"):
        return False
    # validate pdf file exists
    if not os.path.exists(pdf_file_name):
        logger.error(f'{pdf_file_name} does not exist')
        raise ValueError(f'{pdf_file_name} does not exist')

    # always use the trailing / to represent a directory
    save_extract_pdf_folder = f"{save_folder}/adobe_parsed/"
    os.makedirs(save_extract_pdf_folder, exist_ok=True)
    paper_name = helper.get_2nd_last_dir(save_folder)
    zip_abs_path = save_extract_pdf_folder + paper_name + ".zip"

    logger.debug("Start to extract %s to %s", pdf_file_name, zip_abs_path)
    pdf_text_tabel_to_zip(pdf_file_name, save_zip_path=zip_abs_path)
    logger.debug("End to extract %s to %s", pdf_file_name, zip_abs_path)
    all_field_rslts = extract_from_zip(zip_abs_path, oil_field_names,
                                       grouped_by, model,splitter,
                                       token_size, save_folder)
    return all_field_rslts


if __name__ == '__main__':
    pass
