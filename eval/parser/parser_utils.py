"""
Author: Alex <alex.hu@57blocks.com>
Date Created: 2023-10-19
Description: wrapper & utils file.
"""
import re
import numpy as np
import unicodedata
from functools import wraps
from fractions import Fraction
from eval.exception import RESULT_ERROR
from .parser_result import ParseResult, ParserErrorResult
from lib.my_logger import logger

SPLIT_REF_CHAR = "@"
SPLIT_ERROR_CHAR = '$'
COSIN_SIMILARITY_THREADHOLD = 0.91

# key: current unit
# value: target unit required in results
unit_convert_map = {
    "m": "ft",
    "meters": "ft",
    "meter": "ft",
    "metres": "ft",
    "metre": "ft",
    "cm": "in",
    "mpa": "psia",
    "0c": "°f",
    "°c": "°f",
    "⁰c": "°f",
    "c": "°f",
    "oc": "°f",
    "f": "°f",
    "⁰f": "°f",
    "celsius": "°f",
    "degrees-celsius": "°f",
    "degrees-fahrenheit": "°f",
    "bbl": "ton",
    "feet": "ft",  # not need to convert
    "ft": "ft",  # not need to convert
    "°f": "°f",  # not need to convert
    'of': '°f',
    "°-f": "°f",
    "0f": "°f",
    "scf/stb": "scf/bbl oil",
    "water/oil-ratio": "bbl water/bbl oil",
    "bbl-inj/bbl-oil": "bbl water/bbl oil",
    "m3/ton": "scf/bbl oil",
    "kpa": "psia",
    "kpaa": "psia",
    "psi": "psia",
    "psig": "psia",
    "sm3/sm3": "scf/bbl oil",
    "bbl/day": "bbl/d",
    "m3/d": "bbl/d",
    "m3/day": "bbl/d",
    "stb/d": "bbl/d",
    "stb/day": "bbl/d",
    "stb-per-day": "bbl/d",
    "bopd": "bbl/d",
    "bpd": "bbl/d",
    "b/d": "bbl/d",
    "b/day": "bbl/d",
    "mstb/d": "bbl/d",
    "mstb/day": "bbl/d",
    "min-t-of-oil": "bbl/d",
    "stock-tank-barrels-(stb)-per-day": "bbl/d",
    "barrels per day": "bbl/d",
    "k/bpd": "bbl/d",
    "µm²": "md",
    "μm": "md",
    "um2": "md",
    "μm2": "md",
    "µm2": "md",  # different from before 'μm2'
    "%": "mol%",
    "vol%": "mol%",
    "mole-fraction": "mol%",
    "bar": "psia",
}


def handle_parser_error(func):
    '''
    handle any parser error
    '''
    @wraps(func)
    def decorator(self, *args, **kwargs) -> ParseResult:
        try:
            data = func(self, *args, **kwargs)
        except Exception as e:
            tmp = list(args)
            tmp.insert(1, ["", "", ""])
            data = ParserErrorResult.handle_err_response(
                    *tmp, code=RESULT_ERROR, error_stack=str(e),
                    class_name=self.__class__.__name__)
        return data

    return decorator


def unit_convert(value: str, unit: str) -> tuple[bool, any]:
    """
    convert value to the target unit in results
    :param value: value in meters, centimeters, mpa, C, or bbl to convert
    :return: err: if True, conversion failed  (This design is weird)
                  if False, conversion succeeded
             unit: converted value in ft, in, psi, F, or tons
    """
    logger.debug('Start to convert: value: %s unit: %s', value, unit)
    try:
        # value must be a validnumber
        number = float(value)
        unit = str(unit)
    except Exception as e:
        logger.error('Fail to convert %s to float: %s', value, e)
        return True, value

    if unit in ["mpa"]:
        number *= 145
    elif unit in ["cm"]:
        number /= 2.54
    elif unit in ['0c', '°c', '⁰c', 'oc', 'celsius', 'degrees-celsius', 'c']:
        number = (number * 9 / 5) + 32
    elif unit in ['m', 'meters', 'meter', 'metres', 'metre']:
        number *= 3.28
    elif unit in ['kpa', 'kpaa']:
        number *= 0.145038
    elif unit in ['psi', 'psig']:
        number += 14.7
    elif unit in ['sm3/sm3']:
        number *= 5.6146
    elif unit in ['m3/d', 'm3/day']:
        number *= 6.289814
    elif unit in ['min-t-of-oil']:
        number *= 7.46
    elif unit in ['m3/ton']:
        number *= 4.733869973
    elif unit in ['µm²', 'μm2', 'μm', 'um2']:
        number /= 0.9869
    elif unit in ['vol%']:
        number /= 100
    elif unit in ['mole-fraction']:
        number *= 100
    elif unit in ['bar']:
        number *= 14.5
    elif unit in ['mstb/d', 'mstb/day','k/bpd']:
        number *= 1000
    else:
        logger.debug('%s %s do not need convert.', value, unit)

    return False, round(number, 2)


def get_average(height_range: str ,unit: str=None) -> str:
    match = re.match(r'(\d+(?:\.\d+)?)\s*°?\s*([A-Za-z°°µμm²%]+2?)?\s*[-–]\s*(\d+(?:\.\d+)?)\s*°?\s*([A-Za-z°°µμm²%]+2?)'
                     , height_range)
    if match:
        start_number, start_unit, end_number, end_unit = match.groups()
        unit_part = end_unit.strip() or start_unit.strip()
        return f'{round(float(start_number) + (float(end_number) - float(start_number)) / 2, 2)} {unit_part}'

    if unit == 'deg.api':
        pattern_range = r'(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)'
        match = re.match(pattern_range, height_range)
        if match:
            start, end = match.groups()
            return f'{round(float(start) + (float(end) - float(start)) / 2, 2)} {unit}'
    return height_range


def convert_mentioned(s):
    return np.nan if s.strip().lower() == "np.nan" else float(s)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def word_to_number(word):
    word = word.lower().strip()
    word_num = word.split()

    # Dictionary for word representation
    num_dict = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10,
        'eleven': 11,
        'twelve': 12,
        'thirteen': 13,
        'fourteen': 14,
        'fifteen': 15,
        'sixteen': 16,
        'seventeen': 17,
        'eighteen': 18,
        'nineteen': 19,
        'twenty': 20,
        'thirty': 30,
        'forty': 40,
        'fifty': 50,
        'sixty': 60,
        'seventy': 70,
        'eighty': 80,
        'ninety': 90,
    }

    # Multipliers
    mult_dict = {
        'hundred': 100,
        'thousand': 1000,
    }

    if word in num_dict:
        return num_dict[word]

    total = 0
    current_num = 0
    for w in word_num:
        if w in num_dict:
            current_num += num_dict[w]
        elif w in mult_dict:
            current_num *= mult_dict[w]
            total += current_num
            current_num = 0

    return total + current_num


def is_not_mentioned(content: str) -> bool:
    content = content.strip().lower()
    return content in {"not mentioned", "not_mentioned"}


def extract_mixed_numbers(text):
    # parser for mixed numbers like "3-1/2• or 2-7/8"
    pattern = r"(\d+)-(\d+)/(\d+)[”•]?\s*or\s*(\d+)-(\d+)/(\d+)[”•]?"
    if matches := re.search(pattern, text):
        first_mixed_number = _extract_fraction(matches, 1, 2, 3)
        second_mixed_number = _extract_fraction(matches, 4, 5, 6)
        average_mixed_number = (first_mixed_number + second_mixed_number) / 2
        return False, round(float(average_mixed_number), 2)
    return True, None


def _extract_fraction(matches, arg1, arg2, arg3):
    first_whole = int(matches.group(arg1))
    first_numerator = int(matches.group(arg2))
    first_denominator = int(matches.group(arg3))
    return Fraction(
        first_whole * first_denominator + first_numerator, first_denominator
    )

def unicode_fraction_to_float(value):
    """ convert unicode fraction to float """
    match = re.match(r'(\d+)?([^\d]+)?', value)
    if not match:
        return value

    integer_part, fraction_part = match.groups()
    integer_value = int(integer_part) if integer_part else 0

    fraction_value = 0
    if fraction_part:
        fraction_value = sum(unicodedata.numeric(ch) for ch in fraction_part if
                             not ch.isspace())

    return integer_value + fraction_value


def extract_unicode_part(value):
    """ Split unicode part and remaining part """
    import regex as re
    pattern = r'(\X)(\w*)'
    regex = re.compile(pattern, re.UNICODE)
    match = regex.match(value)

    if match:
        return match.group(1), match.group(2)
    return None, None


def parse_unicode_injector_tubing_diameter(content):
    """ Parse Injector tubing diameter value "¼-in" """
    if "-in." in content[0]:
        temp_parse = content[0].replace("-in.", "in")
        # split content into integer and unicode part
        c_temp_parse = temp_parse.split()
        if len(c_temp_parse) > 1:
            integer_part = c_temp_parse[0]
            unicode_part, remain_part = extract_unicode_part(
                c_temp_parse[1])
            if unicode_part:
                c_temp_parse = f"{integer_part}{unicode_part}"
                # convert the fraction to float
                content[0] = unicode_fraction_to_float(
                    c_temp_parse)
                # value includes unit
                if remain_part:
                    content[0] = f'{content[0]} {remain_part}'
                return content
    return None
