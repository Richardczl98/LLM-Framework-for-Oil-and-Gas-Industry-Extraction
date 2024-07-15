# -*- coding: utf-8 -*-
# Author: Anjing Wang
# Date: Aug-08-2023

"""
Helper Functions for simple Text and File Operations
"""

import os
from datetime import datetime
from collections import OrderedDict
from pathlib import Path, PosixPath
from typing import List, Union, Optional
from config import DATA_DIR, RESULT_DIR
import traceback


def str_remove_dup_spaces(mystr: str):
    return ' '.join(mystr.split())


def print_lst_recursive(lst: list):
    assert isinstance(lst, list), "Expected a list as the argument."

    for item in lst:
        if isinstance(item, list):
            print_lst_recursive(item)
        else:
            print(item)
            print('\n')


def get_sorted_filenames(dir_path) -> list:
    """
    List all filenames in the directory
    """
    filenames = os.listdir(dir_path)

    # Sort the filenames
    filenames.sort()

    return filenames


def read_file(filename: str) -> str:
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
    except IOError:
        print(f"Error occurred while reading the file '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return ""


def get_time_str() -> str:
    """
    Return the current timestamp as a string.

    :return: A string representing the current timestamp in the format 'yymmdd_HHMM'.
    :rtype: str
    """
    current_timestamp = datetime.now()
    timestamp_str = current_timestamp.strftime('%y%m%d_%H%M')
    return timestamp_str


def get_time_str_from_path(filepath: Optional[str | Path]) -> str:
    """
    Return the time string from a result final folder name.

    :return: A string representing the timestamp for a result in the format 'yymmdd_HHMM'.
    :rtype: str
    """
    folder_name = Path(filepath).name
    return folder_name.split('-')[0]


def get_file_name_no_ext(filename: str) -> str:
    return os.path.splitext(os.path.basename(filename))[0]


def merge_list_orderdict_to_orderdict(list_of_dicts):
    merged_dict = OrderedDict()

    for od in list_of_dicts:
        for key, value in od.items():
            if key in merged_dict:
                # if key in merged_dict and type(merged_dict[key]) != list:
                if isinstance(merged_dict[key], list):
                    # same key,different value,extend the value list
                    if value[0] not in merged_dict[key] and value != merged_dict[key]:
                        merged_dict[key].extend(value)
                else:
                    if merged_dict[key] != value:
                        merged_dict[key] = [merged_dict[key], value]
            else:
                merged_dict[key] = value

    return merged_dict


def get_paper_name(txt_file_name):
    """
    get paper name for the following dictionary structure
        paper-name.txt
        paper-name/paper.txt
        paper-name/txt/paper.txt
    """
    if txt_file_name.endswith("paper.txt"):
        file_dir = os.path.dirname(txt_file_name)
        parent_dir = os.path.basename(file_dir)
        if parent_dir == "txt":
            grand_parent_dir = os.path.dirname(os.path.dirname(txt_file_name))
            return os.path.basename(grand_parent_dir)

        return parent_dir
    else:
        return get_file_name_no_ext(txt_file_name)


def get_article_name(article_file_path):
    '''
    /path/to/article.txt -> article
    '''
    # Extract the base name of the file (e.g., "article.txt")
    base_name = os.path.basename(article_file_path)

    # Split the base name and the extension
    article_name, _ = os.path.splitext(base_name)

    return article_name



def get_2nd_last_dir(path):
    """
    get 2nd last directory
    """
    # Split the path into parts
    parts = path.split('/')

    # Remove empty parts resulting from trailing or multiple consecutive slashes
    parts = [part for part in parts if part]

    # Check if there are at least two parts
    if len(parts) >= 2:
        return parts[-2]
    return None


import re


def get_first_number(s):
    match = re.search(r'(\d+)', s)
    if match:
        return int(match.group(1))
    return None


def is_number(s) -> bool:
    """
    Check if a given string is a number.

    Args:
        s: could be anything that can be casted to a str

    Returns:
        bool: True if the string is a number, False otherwise.
    """
    s = str(s)
    s = s.replace(',', '')
    try:
        float(s)
        return True
    except ValueError:
        return False


def contains_any(temp_str, lst_C):
    """
    lst_C = ['0c', '°c', '⁰c', 'celsius']

    temp_str = "The temperature is 25°c today."
    result = contains_any(temp_str, lst_C)

    print(result)  # True if temp_str contains any element from lst_C
    """
    for item in lst_C:
        if item in temp_str:
            return True
    return False


def split_at_first_char(str_input: str, char: str) -> str:
    """
    split at first char
    returns the first part and the second part as a list
    """
    parts = str_input.split(char, 1)
    if len(parts) == 2:
        return [parts[0].strip(),
                parts[1].strip()]

    return [parts[0].strip(), '']


def get_extraction(str_input: str) -> str:
    """
    get extraction, which is always the first part
    """
    return split_at_first_char(str_input, '/')[0]


def get_reference(str_input: str) -> str:
    """
    get reference, which is always the second part
    and it could be empty
    """
    return split_at_first_char(str_input, '/')[1]


def get_key(str_input: str) -> str:
    """
    get key of 'key: value'
    """
    return (split_at_first_char(str_input, ':')[0])


def get_value(str_input: str) -> str:
    """
    get value of 'key: value'
    """
    return (split_at_first_char(str_input, ':')[1])


def get_folders_in_path(path: Union[str]) -> List[Path]:
    """
    get all folders in specific path'
    """
    return [Path(path, item) for item in os.listdir(path) if Path(path, item).is_dir()]


def find_ground_truth_files(paper_name: str) -> str:
    '''
    find ground truth file for paper_name
    it should be in ./data/*/ directory
    '''
    paper_short = '-'.join(paper_name.split('-')[:2])
    for root, _, files in os.walk(DATA_DIR):
        for file_name in files:
            # there could be spe_xxx.xlsx.Zone.Identifier file in Windows
            # so we need to make sure the gt file ends with xlsx
            if paper_short.lower() in file_name.lower() and \
                file_name.lower().endswith('.xlsx'):
                return Path(root, file_name).absolute().as_posix()

    raise FileNotFoundError(f'ground truth file for paper {paper_name} not found')


def find_raw_files(location: str = RESULT_DIR) -> List[str]:
    rslts = []
    for root, _, files in os.walk(location):
        for file_name in files:
            if 'extract_raw.xlsx' in file_name.lower():
                rslts.append(Path(root, file_name).absolute().as_posix())
    return rslts


def is_numeric(str_input: str) -> bool:
    ''' True for any valid number include int, float, scientific notation'''
    try:
        float(str_input)
        return True
    except:
        return False


def convert_to_one_if_positive(x):
    if is_numeric(x) and float(x) > 0:
        return 1
    return x


if __name__ == '__main__':
    # print(str_remove_dup_spaces('There are  two     spaces.'))
    # print(get_2nd_last_dir('../data/zips/spe-115712-ms.x/txt/paper.txt'))
    # print(get_reference('jifjeijie/jijfk\/jifjijifeeijfijfiejjifjifeji'))
    pass
