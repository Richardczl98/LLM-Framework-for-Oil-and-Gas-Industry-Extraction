# -*- coding: utf-8 -*-
# Author: Anjing Wang
# Date: Aug-01-2023

"""
prompte template
"""
import os
import sys
from enum import Enum
from typing import List

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')
from lib.my_logger import logger
from lib import helper
from config import YEAR_FOR_CALUCULATION
from schema import variables as vars
from model import prompt_def

STR_REF = 'reference page and reference content'
MAX_REFERENCE = 60
STR_NOT_MENTIONED = 'not_mentioned'

PROMPT_ENFORCE_FORMAT_REF = (
    f'When user asks "{STR_REF}", '
    'user wants to know the reference you used to reasoning about the answer. '
    f'It is not ask you to output the literal string of "{STR_REF}". '
    'Save the reference text (not line numbers) '
    'from which you extracted the answer '
    'to "reference content"; '
    'and save the reference text\'s page number to "reference page". '
    f'Make sure to keep the reference text under {MAX_REFERENCE} words, '
    'as we have limited output space. '
    'Ignore any line breakers in reference text, '
    'and output them as a single line. '
    'When you cannot extract the answer, '
    'please only output as required, which is usually '
    f'{{key:{STR_NOT_MENTIONED}}} and do not need to give any explanations. '
    f'"{STR_REF}" is specific for every question, '
    'so work on it every time when you answer a question. '
)

PROMPT_REF_REMINDER = (
    f'You need to replace {STR_REF} properly as required every time '
    'you answer a question and follow all format requirements. '
    'Refer to the beginning of the prompt '
    'for instructions and examples. '
    f'DO NOT just output the literal string of "{STR_REF}". '
)

PROMPT_ENFORCE_SPACE_VAL_UNIT = (
    'make sure only one space between the "value" and the "unit". '
)

PROMPT_ENFORCE_FORMAT_BRACES = (
    'We always ask you to answer in the following format: '
    f'{{key:value unit@{STR_REF}}}. '
    'Please note for some questions, only value exsit, and unit does not exsit. '
    f'If unit exsit, {PROMPT_ENFORCE_SPACE_VAL_UNIT}'
    'Always output the curly braces, which enclose the answer; '
    'do not add punctuation or any extra text outside of the curly braces; '
    'and we rely on the curly braces to seperate and parse the answer. '
    'Within the curly braces, text before ":" is the key '
    'we use to recognize the question. The key should be kept exactly as it is. '
    'Text after ":" and before "@" is the value and unit '
    '(if exsit) of the key or what we ask you to extract from the papers. '
    f'Text after "@" is {STR_REF} that let us know where the answer comes from. '
    f'{PROMPT_ENFORCE_FORMAT_REF}\n'
    'Here is an example: '
    'The reference text says "the Oska field\'s oil production volume is 23 bbl/day" in page 1  , '
    'and user ask what is the Oil production volume for the Oska field? '
    'you should answer in the following format: '
    '{Oil production volume:23 bbl/day@'
    'page 1 the Oska field\'s oil production volume is 23 bbl/day}. '
)


PROMPT_ENFORCE_NO_FUTURE = (
    'Do not extract infromation that is an estimation '
    'in the future. '
)


PROMPT_ENFORCE_FORMAT_NO_OWN_WORDS = (
    'Do not rely on other external resources. '
    'Only answer strictly with the following formats '
    'defined within the curly braces. '
    'Do not use your own formats to answer. '
)


PROMPT_ENFORCE_NUMERIC = (
    'Always answer in the numeral form, such as 8 instead of eight. '
)


PROMPT_EXAMPLE_NO_RELATIVE_NUM = (
    'Do not extract a relative number. '
    'For example, if you encounter "40 higher than the orignal value", '
    'do not extract 40 since it\'s a relative value. '
    'We need to alwaysextract an absolute value. '
)


PROMPT_EXAMPLE_NO_RANGE = (
    'Do not extract standalone numbers '
    'when they are part of a phrase indicating a range. '
    'For example, avoid extracting "1000" '
    'when it is used within the phrase "more than 1000" '
    'Instead, extract the entire phrase "more than 1000". '
    'Similarly, avoid extracting "1000" from expressions like "less than 1000". '
    'Instead, extract the entire phrase "less than 1000". '
    'Similarly, extract the entire phrase "between 1000 and 2000", which indicates a range. '
)


def pt_extract_val_unit_part_1(key: str, eo_field: str):
    ''' val + unit style - part 1 '''
    prompt = (
        'From the above reference text, '
        f'extract the "value" and the "unit" of {key.lower()} in {eo_field}. '
    )
    return prompt


def pt_extract_val_unit_part_2(key: str):
    ''' val + unit stype - part 2 '''
    prompt = (
        'If you are able to extract, '
        f'please answer {{{key}:value unit@Reference page and reference text}}, '
        f'Otherwise, please answer {{{key}:not_mentioned}}. '
    )
    return prompt


def pt_extract_val_unit(key:str, eo_field:str, finetune:str = ''):
    ''' val + unit style '''
    prompt = pt_extract_val_unit_part_1(key, eo_field)
    prompt += finetune
    prompt += pt_extract_val_unit_part_2(key)
    return prompt


# we add format enforcement to system message
# to ensure that the format of system message is correct
# it is added at the beginning of the user message as well
SYS_MSG_EXTRACTOR = (
        'You are Opgie, an AI assistant to help researchers extracting information '
        'from provided reference texts. '
        'Use your knowledge of gas and oil fields '
        'to understand questions and the reference material. '
        'But only extract information that is explicitly stated '
        'in the reference text and avoid conjecture. '
        'Providing fabricated results compromises the integrity of the research '
        'and makes the extraction process inefficient. '
        'Do not extract information that is an estimate in the future. '
        'Do not rush to answer, and always think through questions. '
        'Accuracy is way more important than speed. '
        'When you are not confident about the accuracy of the extraction, '
        'treat it like you cannot extract. '
        'For our project, false positive is much worse than false negative. '
        f'{PROMPT_ENFORCE_FORMAT_BRACES}'
    )

SYS_MSG_FORMATTER = (
    'You are an assistant to help reformat the provided text. '
    'Only change the formatting and units according to directions and '
    'do not modify any {key:value} unless instructed to do so '
    'and only return the formatted text.  '
    'You need to remember that your name is Opgie.'
    )

SYS_MSG_ASSISTANT = 'You are a helpful AI assistant to answer questions'
SYS_MSG_ASSISTANT = helper.str_remove_dup_spaces(SYS_MSG_ASSISTANT)

SYS_MSG_GEOGRAPHY_EXPERT = "You are now a geography savvy expert to answer questions. "


class GroupedBy(Enum):
    '''group questions by section or individual'''
    SECTION = 1
    INDIVIDUAL = 2


def pt_extract_country_and_compare_question(country_1: str, country_2: str):
    return f"""
    Are extracted country from {country_1} and extracted country from {country_2} same country?
    If they are same country, please output {{"answer": true}}; otherwise output {{"answer": false}}.
    (Please keep the curly braces in the answer, and do not output any other unrelated information.)
    """


def pt_concatenate_question_ref(question:str, ref:str):
    '''
    concatenate question and reference together
    by the following fixed format
    '''
    # if not question or not isinstance(question, str):
    #     raise ValueError("The question must be a valid non-empty string.")

    # if not ref or not isinstance(ref, str):
    #     raise ValueError("The reference must be a valid non-empty string.")

    conactenated = (
        '### Start of the Reference Text ###\n'
        f'{ref}\n'
        '### End of the Reference Text ###\n'
        f'{question}'
    )
    logger.debug('question: %s\n', conactenated)
    return conactenated


# we make up a prefix to clearly lable the object we target
# eo_: extraction object
def is_a_as_part_of_b_for_field(eo_a: str, eo_b: str, eo_field: str):
    ''' template for a as part of b for field '''
    question = (
        f'Is {eo_a} mentioned in the above reference text '
        f'as {eo_b} for {eo_field}? '
        'If it is mentioned, '
        f'please answer {{{eo_a}:mentioned@Reference page and reference content}}. '
        f'Otherwise, please answer {{{eo_a}:not_mentioned}}. '
    )
    return question


def what_type_of_a_for_field(eo_field: str,
                             eo_a: str,
                             types: list,
                             what_question: str = 'What is it? ', ):
    question = (
            f'From the above reference text, '
            f'extract the type of {eo_a} that used for {eo_field}; '
            f'type could be one of {", ".join(types)}, {what_question} '
            'If you can extract, '
            f'please answer {{{eo_a}:value@Reference page and referece content}}. '
            f'Otherwise, please answer {{{eo_a}:not_mentioned}}. '
        )
    return question


def what_a_for_field(eo_field: str,
                     eo_a: str,
                     year_txt:str='',
                     what_question: str = 'what is it? ',
                     unit_question: str = ''):
    '''prompt template for what a for field'''
    prompt = (
        'From the above reference text, '
        f'extract {eo_a} for {eo_field}{year_txt}, '
        f'{what_question} {unit_question}'
        'If you can extract, '
        f'please answer {{{eo_a}:value@Reference page and reference content}}. '
        f'Otherwise, please answer {{{eo_a}:not_mentioned}}. '
    )
    return prompt


def fill_year(year = None):
    ''' fill year if it is requireed'''
    if year:
        # space is put in the front on purpose
        return f' in the year of {year}'

    return ''


def common_template(*notice, unit=False, eo_field=None, field_name=None, extra_time=None):
    notice = ','.join(notice)
    if unit:
        question = (f'From the above reference text, if you can extract {field_name} for {eo_field}, {notice}'
                    f'provide the "value" and "unit" in the format {{{field_name}:value UNIT@Reference page and content}} '
                    'Otherwise, please answer {{{field_name}:not_mentioned}}'
                    ) if not extra_time else \
                    (f'From the above reference text, in the {extra_time},'
                     f'if you can extract {field_name} for {eo_field} for the {extra_time}, {notice}'
                     f'provide the value and unit in the format {{{field_name}:value UNIT@Reference page and content}},'
                     f'Keep the reference text under {MAX_REFERENCE} words,Otherwise, please answer {{{field_name}:not_mentioned}}'
                     f',Please use curly braces to enclose the answer.')

    else:
        question = (f'From the above reference text,if you can extract {field_name} for {eo_field}, {notice}'
                    f'please answer {{{field_name}:value@Reference page and content}},Keep the reference text under'
                    f' {MAX_REFERENCE} words,Otherwise, please answer {{{field_name}:not_mentioned}}' \
                    f' Please use curly braces to enclose the answer.') if not extra_time else \
                    (f'From the above reference text, in the {extra_time},'
                     f'if you can extract {field_name} for {eo_field} for the {extra_time}, {notice}'
                     f'please answer {{{field_name}:value@Reference page and content}},Keep the reference text under {MAX_REFERENCE} words,Otherwise, please answer {{{field_name}:not_mentioned}}'
                     f',Please use curly braces to enclose the answer.')

    return question


# pt prefix + section number + attr-var-name + w_year
# all other functions please follow the naming convention
def pt_sec1_downhole_pump(eo_field: str, year=None):
    '''section 1 - attr 1
    prompt for downhole pump'''
    qst = (
        'According to the above reference text, '
        f'is downhole pump used in {eo_field}? '
        'If yes, please answer '
        '{Downhole pump:mentioned@Reference page and referece content}. '
        'If no, please answer {Downhole pump:not_mentioned}. '
        'I\'ll gvie you a few hints to help you answer better. '
        'Hint 1: '
        'Please note that there are several types of downhole pumps, '
        'such as Rod Pump, Sucker Rod Pump or '
        'Electric Submersible Pump (ESP). '
        'So they may not mention the text "downhole pump", '
        'but they may mention a specific type of downhole pump. '
        'Hint 2: '
        'Sometimes they mention downhole pump or a type of downhole pump, such as '
        'Rod Pump is used in Basin A, and the field B is located in Basin A. '
        'You\'ll need to take extra reasoning steps to figure out that '
        'field B uses downhold pump, and answer accordingly. '
    )
    return qst


def pt_sec1_water_reinjection(eo_field: str, year=None):
    '''
    prompt for water reinjection
    '''
    question = (
        f'From the above reference text, '
        f'does {eo_field} oil field adopt water reinjection '
        'as a production method for oil or gas exploitation? '
        'Please note that water injection for water flooding is not water reinfection, '
        'maintaining reservoir pressure is equal to water flooding, '
        'not water reinjection is equal to water disposal, '
        'water flooding and water reinjection are two completely different ways. '
        'please answer {Water reinjection:mentioned@Reference page and content}. '
        'Otherwise, please answer {Water reinjection:not_mentioned}. '
    )
    return question

def pt_sec1_natural_gas_reinjection(eo_field: str, year=None):
    '''section 1 - attr 3'''
    qst = is_a_as_part_of_b_for_field(vars.VAR_SEC1_NATURAL_GAS_REINJECTION,
                                       'a production method',
                                       eo_field)
    return qst

def pt_sec1_water_flooding(eo_field: str, year=None):
    '''section 1 - attr 4'''
    qst = is_a_as_part_of_b_for_field(vars.VAR_SEC1_WATER_FLOODING,
                                       'a production method',
                                       eo_field)
    return qst

def pt_sec1_gas_lifting(eo_field: str, year=None):
    '''section 1 - attr 5'''
    qst = is_a_as_part_of_b_for_field(vars.VAR_SEC1_GAS_LIFTING,
                                       'a production method',
                                       eo_field)
    return qst

def pt_sec1_gas_flooding(eo_field: str, year=None):
    '''section 1 - attr 6'''
    qst = is_a_as_part_of_b_for_field(vars.VAR_SEC1_GAS_FLOODING,
                                       'a production method',
                                       eo_field)
    return qst


def pt_sec1_steam_flooding(eo_field: str, year=None):
    '''section 1 - attr 7'''
    qst = is_a_as_part_of_b_for_field(vars.VAR_SEC1_STEAM_FLOODING,
                                       'a production method',
                                       eo_field)
    return qst


def pt_sec1_oil_sands_mine_i(eo_field: str, year=None):
    '''section 1 - attr 8'''
    qst = is_a_as_part_of_b_for_field(vars.VAR_SEC1_OIL_SANDS_MINE_I,
                                       'a production method',
                                       eo_field)
    return qst

def pt_sec1_oil_sands_mine_ni(eo_field: str, year=None):
    '''section 1 - attr 9'''
    qst = is_a_as_part_of_b_for_field(vars.VAR_SEC1_OIL_SANDS_MINE_NI,
                                       'a production method',
                                       eo_field)
    return qst


def pt_sec1_production_method(eo_field: str, year = None):
    '''prompt for section 1: production method'''
    logger.info('Start to prepare section 1 prompts for %s', eo_field)
    q_pm=[]
    q_pm.append(pt_sec1_downhole_pump(eo_field))                #1
    q_pm.append(pt_sec1_water_reinjection(eo_field))            #2
    q_pm.append(pt_sec1_natural_gas_reinjection(eo_field))      #3
    q_pm.append(pt_sec1_water_flooding(eo_field))               #4
    q_pm.append(pt_sec1_gas_lifting(eo_field))                  #5
    q_pm.append(pt_sec1_gas_flooding(eo_field))                 #6
    q_pm.append(pt_sec1_steam_flooding(eo_field))               #7
    q_pm.append(pt_sec1_oil_sands_mine_i(eo_field))             #8
    q_pm.append(pt_sec1_oil_sands_mine_ni(eo_field))            #9
    combined_prompt = pt_combine_individuals(q_pm)
    return combined_prompt


def pt_combine_individuals(lst_q):
    '''combine individual questions into a long prompt.'''
    combined_prompt = (
        'Answer the following questions one by one. '
        'Answer every question independently '
        'and it shall not be affected by other questions. '
        'DO NOT ignore or omit any questions, ALL questions '
        'need to be answered even if you cannot extract. '
        'Follow the instruction to answer if you cannot extract. '
        'Answer every question only once, '
        'and do not repeat the answer multiple times. '
        'Ensure every answer is on a separate row. \n'
        f'{PROMPT_ENFORCE_FORMAT_BRACES}'
    )
    q_prefix = (
        '\nThis is the start of a question. '
        'This question can not be skipped, please answer it. '
        'After answering this question, '
        'go ahead to answer the next question if it exists.'
        f'{PROMPT_REF_REMINDER}'
    )
    combined_prompt += q_prefix
    combined_prompt += q_prefix.join(lst_q)
    return combined_prompt


def pt_standardize_text(eo_response: str):
    txt = f'''For the following text: {eo_response}, please reformat the text so that key:value pairs are separated by a
colon :, and the key:value pairs are enclosed in curly braces. Please add curly braces if they do not exist. If a value
is "not mentioned", please replace the space with an underscore, ie: not_mentioned.'''
    return txt


def pt_temperature_format_text():
    txt = f'''For the text provided above, if there exists a unit for {{reservoir temperature: value}} and the unit is in Celsius, \
    please reformat the unit to be 0c with a space between the number and unit. NO UNDERSCORES. \
    Example correct formatting: 24 0c. If the value is not_mentioned then do not reformat'''
    return txt


def pt_get_missing_units_text(eo_units: str, eo_response: str):
    txt = f'''Given the following {{key:value}} pairs: {eo_response}, for the following keys: {" ,".join(eo_units)},
    please find the missing units for the values from the reference text(s) previously provided and attach the units to the values.
    Return the text in its original formatting with the added units. Please use unit shorthands.'''
    return txt

def pt_sec2_field_location(eo_field: str, year=None):
    '''prompt for country'''
    qst = (
        f'Please extract the country where {eo_field} is located, '
        'based on the above reference text. '
        'If you do not find country directly, but can find the state or province, '
        'you may use your knowledge to answer the country. '
        'For example, if it is located in California, you may answer the United States of Amercia; '
        'if it is located in Heilongjiang, you may answer China. '
        'If you find a country, save it to "value". '
        'Then output {Field location (Country):value@Reference page and referece content}, '
        'Please note "Field location (Country)" in the above {} before : is the key, '
        'and do not put your answer here. '
        'You should put answer to "value" in the above {}. '
        'If you do not find country, answer {Field location (Country):not_mentioned}. '
    )
    return qst

def pt_sec2_field_name(eo_field: str, year=None):
    ''' prompt for field name '''
    prompt = f'{prompt_def.PROMPT_MAGIC_RETURN_REST} {{{vars.VAR_SEC2_FIELD_NAME}:{eo_field}}}'
    return prompt

def _pt_sec2_filed_age_no_year(eo_field: str):
    prompt = (
        'From the above reference text, extract field age. '
        'Field age is defined as the number of years '
        f'that have passed since the {eo_field} Field '
        f'initially started its production of oil or gas, up to the year of {YEAR_FOR_CALUCULATION}. '
        'Please note we are not interested in when the field was discovered, '
        'but need to know the actual year of start of oil (or gas) production. '
        'You also need to a simple calculation. '
        'For example, if the first production was in 2000, '
        f'the field age is {YEAR_FOR_CALUCULATION} - 2000 = 23. '
        'Please make sure to use the year of first production to caculate. '
        'For example, if you encounter text like '
        '"this field has been steamflooded for 20 years", '
        'You should not extract 20 years as the field age, '
        'because steamflooding could be only part of the production, not the entire part. '
        'If you are able to extract the field age, '
        'please answer {Field age:value@Reference page and refrence content}. '
        'Otherwise, please answer {Field age:not_mentioned}. '
    )
    return prompt


def pt_sec2_field_age_w_year_in_section(eo_field: str, year: int=None):
    ''' prompt for field age '''
    if year is None:
        return _pt_sec2_filed_age_no_year(eo_field)
    else:
        field_age = YEAR_FOR_CALUCULATION - year
        prompt = ('For this question, you do not need to look at the above reference text. '
                f'Please answer {{{vars.VAR_SEC2_FIELD_AGE}:{field_age}}} '
                 'Do not need to reason and just answer with the above curly braces, '
                 'and the literal content inside them. Please do not output anything else.')
        return prompt


def pt_sec2_field_age_w_year_individual(eo_field: str, year: int=None):
    ''' prompt for field age '''
    if year is None:
        return _pt_sec2_filed_age_no_year(eo_field)
    else:
        field_age = YEAR_FOR_CALUCULATION - year
        prompt = f'{prompt_def.PROMPT_MAGIC_RETURN_REST} {{{vars.VAR_SEC2_FIELD_AGE}:{field_age}}} '

        return prompt


def pt_sec2_field_depth(eo_field, year=None):
    '''
   field depth prompt
    '''
    prompt = (
        f'From the above reference text, if you can extract field depth '
        f'of {eo_field}, answer {{Field depth:value unit@{STR_REF}}}. '
        'Otherwise, answer {Field depth:not_mentioned}. '
        'Please use the following guidance: '
        '1. field depth is not the well depth. Do not confuse them. '
        'Well depth is the actual depth of a particular well, '
        'while field depth is the depth of the average or typical depth range '
        'at which the gas/oil-bearing formations are found '
        'within a specific gas/oil field. '
    )

    return prompt


def pt_sec2_production_volume_w_year(eo_field: str,
                                 year_txt=None):
    '''prompt for oil production volume'''
    prompt = (
        'From the above reference text, '
        f'extract the number of oil production volume of {eo_field}{year_txt}. '
        'If we ask you oil production volume in a particular year,'
        'it does not mean you have to give the volume for the entire year. '
        'If you can just extract the oil production volume in any period of that year, '
        'that is what we need. '
        'For example, you can extract 23 bbl/day from text like '
        '"the oil production volume is 23 bbl/day at the begining of the year". '
        'If you can extract, '
        'provide the "value" and "unit" in the format of '
        '{Oil production volume:value unit@Reference page and content}. '
        'If the oil production volume is not in a specific time, '
        'but in an accumulated period, '
        'give out the answer in the format of '
        '{Oil production volume:value unit within the accumulated period@Reference page and content}. '
        'For example, extract or summarize "23 million barrels since the inception of the oil field" '
        'if it is expressed in the referece text. Make sure always follow the format requirement.'
        'If you were not able to extracte a number in a specific time or within an accumulated period, '
        'answer {Oil production volume:not_mentioned}. '
        'Please note that oil production volume is '
        'NOT the recoverable reserves estimation. It\'s the volume that has been produced.'
    )
    return prompt


def pt_sec2_num_of_producing_wells_w_year(eo_field: str,
                                       year_txt=None):
    '''prompt for number of produding well'''
    prompt = (
        'From the above reference text, '
        f'extract the number of producing wells of {eo_field}{year_txt}. '
        f'{PROMPT_ENFORCE_NUMERIC}'
        'If you encounter any text like "six out of eight producing well", '
        'the answer is 8. Do not output 6 or "six out of eight". '
        'What we need is the total number. '
        f'{PROMPT_EXAMPLE_NO_RANGE}'
        'Ignore any context like six producing well is redrilled.'
        'Again, we need to extract the total number not the partical number. '
        'The number of redrilled producing well does not refect the total number. '
        'Please note that producing wells are sometimes called '
        'active producers or simply produers. '
        'Do not confuse well slots with the producing wells since well slots might include '
        'other type of wells, such as water injecting wells. '
        'What we need is the number of producing wells. '
        'Another example is that you can extract 10 from text like '
        '"out of 21 active wells 10 are producers and 11 are injectors". '
        '10 is still the totoal number of producing well. '
        '21 is the total number of wells including producers and injectors, '
        'but we do not need to extract 21.'
        'If you were able to extracte the number, '
        'answer {Number of producing wells:value@Reference page and content}. '
        'If you were not able to extracte the number, '
        'answer {Number of producing wells:not_mentioned}. '
    )
    return prompt


def pt_sec2_num_of_water_injecting_wells_w_year(eo_field: str,
                                               year_txt=None):
    '''prompt for number of water injecting well'''
    prompt = (
        'From the above reference text, '
        f'extract the number of water injecting wells of {eo_field}{year_txt}. '
        f'{PROMPT_ENFORCE_NUMERIC}'
        'If you encounter any text like "six out of eight water injecting well", '
        'the answer is 8. Do not output 6 or "six out of eight". '
        'What we need is the total number. '
        'Ignore any context like six water injecting well is redrilled.'
        'Again, we need to extract the total number not the partical number. '
        'The number of redrilled water injecting well does not refect the total number.'
        'Do not extract a range number such as 1000 out of "more than 1000", '
        'as we need to extract exact number, not a range. '
        'Please note that water injecting wells are sometimes called injectors. '
        'But please make sure the injectors refer to water injecting wells, not other injectors. '
        'Do not confuse well slots with water injecting wells since well slots might include '
        'other type of wells, such as producing wells. '
        'What we need is the number of water injecting wells. '
        'Do not get confused between injecting well and injection manifolds, '
        'they are two different things. '
        'Another example is that you can extract 11 from text like '
        '"out of 21 active wells 10 are producers and 11 are injectors". '
        '11 is still the totoal number of water injecting wells. '
        '21 is the total number of wells including producers and injectors, '
        'but we do not need to extract 21.'
        'If you were able to extracte the number, '
        'answer {Number of water injecting wells:value@Reference page and content}. '
        'If you were not able to extracte the number, '
        'answer {Number of water injecting wells:not_mentioned}. '
    )
    return prompt


def pt_sec2_production_tubing_diameter(eo_field: str, year=None):
    ''' prompt for production tubing diameter '''
    prompt = what_a_for_field(eo_field,
                     vars.VAR_SEC2_PRODUCTION_TUBING_DIAMETER)
    return prompt


def pt_sec2_injector_tubing_diameter(eo_field: str, year=None):
    ''' prompt for injector tubing diameter '''
    prompt = what_a_for_field(eo_field,
                     vars.VAR_SEC2_INJECTOR_TUBING_DIAMETER)
    return prompt


def pt_sec2_bottomhole_pressure(eo_field: str, year=None):
    ''' prompt for bottomhole pressure '''
    prompt = what_a_for_field(eo_field,
                     vars.VAR_SEC2_BOTTOMHOLE_PRESSURE)
    return prompt


def pt_sec2_reservoir_pressure(eo_field: str, year=None):
    ''' prompt for bottomhole pressure '''
    prompt = what_a_for_field(eo_field,
                     vars.VAR_SEC2_RESERVOIR_PRESSURE)
    prompt = prompt.replace('Please use curly braces',
                              ('Please also answer {Reservoir pressure:not_mentioned} '
                               'if only pressure at bubble point is extracted. '
                               'Please use curly braces'))
    return prompt


def pt_sec2_reservoir_temperature(eo_field: str, year=None):
    ''' prompt for bottomhole pressure '''
    prompt = what_a_for_field(eo_field,
                     vars.VAR_SEC2_RESERVOIR_TEMPERATURE)
    prompt += (' If you cannot directly extract the unit for the temperature, '
               'please try to decide the unit by the context of paper to be 0C or 0F.')
    return prompt


def pt_sec2_offshore(eo_field: str, year=None):
    '''prompt for offshore'''
    qst = (
        'From the above reference text, '
        'please extract the physical location '
        f'(land or sea, not country or state/province) of {eo_field}. '
        'If the physicallocation is not mentioned, '
        'just answer {Offshore:not_mentioned}. '
        'If the physical location is mentioned, '
        'rember this location, but do not output it. '
        'A hint for you that if you encounter '
        'any text like \'the field under discussion\', '
        'you\'ll need take extra effort to figure out what field it is. '
        'If the location is on land or onshore, '
        'such as deserts, forests, plains or land basins, '
        'please answer {Offshore:0@Reference page and content}, '
        'If the location is in the sea or offshore, '
        'please answer {Offshore:1@Reference page and content}. '
    )

    return qst


def pt_sec2_field_properties(eo_field: str, year=None):
    ''' question of field properties'''
    logger.debug('eo_field: %s, year: %s', eo_field, year)

    q_fp = []
    q_fp.append(pt_sec2_field_location(eo_field))  # 0: country

    year_txt = fill_year(year)
    qst = pt_sec2_field_age_w_year_in_section(eo_field, year) #1
    q_fp.append(qst)

    # e.g. spe-87016 1000+50/2, 1000 is not correctly extracted
    qs = pt_sec2_field_depth(eo_field) # 2. field depth
    q_fp.append(qs)

    qs = pt_sec2_production_volume_w_year(eo_field, year_txt) #3
    q_fp.append(qs)

    qs = pt_sec2_num_of_producing_wells_w_year(eo_field, year_txt) #4
    q_fp.append(qs)

    qs = pt_sec2_num_of_water_injecting_wells_w_year(eo_field) #5
    q_fp.append(qs)

    q_fp.append(pt_sec2_production_tubing_diameter(eo_field)) #6
    # TODO: Injector tubing diameters spe-140630 need support A or B
    q_fp.append(pt_sec2_injector_tubing_diameter(eo_field)) #7
    q_fp.append(pt_sec2_bottomhole_pressure(eo_field)) #8
    q_fp.append(pt_sec2_reservoir_pressure(eo_field)) #9
    q_fp.append(pt_sec2_reservoir_temperature(eo_field)) #10
    q_fp.append(pt_sec2_offshore(eo_field)) #11
    ret = pt_combine_individuals(q_fp)
    return ret


def pt_sec3_api_gravity(eo_field: str, year=None):
    ''' prompt of api gravity '''
    prompt = (
        f'\nFrom the above reference text, if you can extract the API or API gravity "value" and the "unit" for '
        f'the "oil" or "dead oil" in {eo_field} at standard pressure and temperature,'
        f'please answer {{{vars.VAR_SEC3_API_GRAVITY}:value unit@Reference page and reference text}}, '
        f'otherwise, please answer {{{vars.VAR_SEC3_API_GRAVITY}:not_mentioned}}. '
        f'Please use curly braces to enclose the answer and make sure only one space between the "value" and the "unit". '
        f'Please keep the reference text under {MAX_REFERENCE} words.'
    )
    return prompt

def gas_composition_prompt(eo_field: str,
                           gas: str,
                           description: str = '') -> str:
    ''' prompt template for gas composition '''
    prompt = (
        'From the above reference text, '
        'please extract or caculate the value and unit '
        'of natrual gas composition of '
        f'{gas}{description} for {eo_field}. '
        'The unit is usually "mol%" or "% volume" '
        'Only use one of them as the unit. If you cannot decide '
        'which unit should use, ignore the unit part. '
        'Never use percentage sign (%) or percent alone as the unit. '
        'The value is the numerical part of percentage. '
        'For example, if the extracted is '
        '2 mol%, 2 % volume, 2 %, 2% or 2 percent, '
        'the value is 2, not 0.02, not 2%. '
        'There is one caculation you might need to take care. '
        'If we want to extract "C4+", '
        'but the reference text gives "C4" and "C5+", '
        'you need to add "C4" and "C5+" together to get "C4+" '
        'and output the sum as the caculated value. '
        'If you can extract or caculate, answer '
        f'{{{gas}: value unit@Reference page and Reference content}} '
        'If you cannot extract or caculate, '
        f'answer {{{gas}: not_mentioned}}. '
    )
    return prompt


def pt_sec3_n2(eo_field: str, year=None):
    ''' prompt of n2 '''
    return gas_composition_prompt(eo_field, vars.VAR_SEC3_N2, '')


def pt_sec3_co2(eo_field: str, year=None):
    ''' prompt of n3 '''
    return gas_composition_prompt(eo_field, vars.VAR_SEC3_CO2, '')


def pt_sec3_c1(eo_field: str, year=None):
    ''' prompt of c1 '''
    return gas_composition_prompt(eo_field, vars.VAR_SEC3_C1, '')


def pt_sec3_c2(eo_field: str, year=None):
    ''' prompt of c2 '''
    return gas_composition_prompt(eo_field, vars.VAR_SEC3_C2, '')


def pt_sec3_c3(eo_field: str, year=None):
    ''' prompt of c3 '''
    return gas_composition_prompt(eo_field, vars.VAR_SEC3_C3, '')


def pt_sec3_c4_plus(eo_field: str, year=None):
    ''' prompt of c4+ '''
    return gas_composition_prompt(eo_field,
                                  vars.VAR_SEC3_C4_PLUS,
                                  '(Alkanes with 4 and MORE carbon atoms)')


def pt_sec3_h2s(eo_field: str, year=None):
    ''' prompt of h2s '''
    return gas_composition_prompt(eo_field, vars.VAR_SEC3_H2S, '')


def pt_sec3_fluid_properties(eo_field: str,
                             year=None):
    ''' prompt of fluid properties '''
    q_fp = []
    q_fp.append(pt_sec3_api_gravity(eo_field))
    q_fp.append(pt_sec3_n2(eo_field))
    q_fp.append(pt_sec3_co2(eo_field))
    q_fp.append(pt_sec3_c1(eo_field))
    q_fp.append(pt_sec3_c2(eo_field))
    q_fp.append(pt_sec3_c3(eo_field))
    q_fp.append(pt_sec3_c4_plus(eo_field))
    q_fp.append(pt_sec3_h2s(eo_field))

    combined_prompt = pt_combine_individuals(q_fp)
    return combined_prompt


def field_name():
    txt='''According to the above text, which oil fields are highlighted in the text?Please output in json format.
    Key is Oil_fields and field name does not end in field.
    '''
    return helper.str_remove_dup_spaces(txt)


def pt_sec9_oil_production_bopd(eo_field, year:int=None):
    ''' section 9 - helpers - prompt of oil production bopd '''
    year_txt = fill_year(year)
    txt = f'''From the above reference text,how much oil was produced（withdrawal rate）in the {eo_field} field {year_txt}, in barrels of oil per day(BOPD for short).
    Please answer{{Oil_Production_BOPD:value BOPD@Reference page and content}},Keep the reference text under 40 words,
    Otherwise, please answer{{Oil_Production_BOPD:not_mentioned}} Please use curly braces to enclose the answer.
    '''
    return helper.str_remove_dup_spaces(txt)


def pt_sec9_gas_production_mmscfd(eo_field, year:int=None):
    ''' section 9 - helpers - prompt of oil production mmscfd '''
    year_txt = fill_year(year)
    txt = f'''From the above reference text, how much gas was produced（withdrawal rate）in the {eo_field} field {year_txt}, in millions of cubic feet per day(Mmscfd for short).
    Please answer{{Gas_Production_Mmscfd:value Mmscfd@Reference page and content}},Keep the reference text under 40 words,
    Otherwise, please answer{{Gas_Production_Mmscfd:not_mentioned}} Please use curly braces to enclose the answer.
    '''
    return helper.str_remove_dup_spaces(txt)

def pt_sec4_gor(eo_field, year:int=None):
    ''' prompt of GOR '''
    # Ratio will be caculated if cannot be extracted:
    # refer to spe9478, news-TRN09
    year_txt = fill_year(year)
    txt=f'''From the above reference text, if you can extract Gas-to-oil ratio (GOR) for {eo_field}{year_txt}, that specifically refers to free gas and excludes any mention of solution GOR, provide the "value" and "unit" in the format {{Gas-to-oil ratio (GOR):value UNIT@Reference page and content}},
    Keep the reference text under 40 words. Otherwise, please answer {{Gas-to-oil ratio (GOR):not_mentioned}},
    Please use curly braces to enclose the answer.
    '''
    return helper.str_remove_dup_spaces(txt)


def pt_sec4_wor_w_year(eo_field:str, year:int=None):
    '''
    section 4: production practice
    Water-to-oil ratio (WOR)
    unit: bbl water/bbl oil
    Definition: wor = water production volume / oil production volume
    '''
    # TODO: ratio needs to be caculated: refer to spe9478
    # in 1972, 90,000 bbl/day / 14,000 bbl/day = 6.4285
    # oil production volume in 1972 is 90,000 bbl / day
    # we might need step-extraction and then calcualte the ratio
    # for now, use the prompt only

    year_txt = fill_year(year)
    prompt = (
            'From the above reference text, '
            f'Extract and caculate Water-to-oil ratio (WOR) for {eo_field}{year_txt}, '
            'which is the water production divided by the oil production. '
            'If you can extract and caculate the value, '
            'provide the "value" and "unit" in the format of '
            '{Water-to-oil ratio (WOR):value unit@Reference page and content}. '
            'Otherwise, please answer {Water-to-oil ratio (WOR):not_mentioned}. '
        )
    return prompt


def pt_sec4_water_injection_ratio_w_year(eo_field:str, year:int=None):
    ''' prompt of water injection ratio '''
    # TODO: ratio needs to be caculated and defined Inject rate over produced oil volume
    year_txt = fill_year(year)
    prompt = ('Water injection ratio is defined as the volume of water injected '
              'over the volume of oil produced. '
              'From the above reference text, '
              f'if you can extract Water injection ratio for {eo_field}{year_txt}, '
              'what is it? what unit is it? '
              'Please answer {Water injection ratio:value@Reference page and content}. '
              'Otherwise, answer {Water injection ratio:not_mentioned}. '
              'Please note that water injection rate refers to the speed or volume '
              'at which water is injected into an oil reservoir. '
              'Water injection rate is not water injection ratio, '
              'please do not get confused with those two terms.')
    return prompt


def pt_sec4_gas_lifting_injection_ratio_w_year(eo_field:str, year:int=None):
    year_txt = fill_year(year)
    txt=f'''From the above reference text, if you can extract Gas lifting injection ratio for {eo_field}{year_txt}, what is it? what unit is it?
    please answer {{Gas lifting injection ratio:value@Reference page and content}},Keep the reference text under 40 words,Otherwise,
    please answer {{Gas lifting injection ratio:not_mentioned}} Please use curly braces to enclose the answer.'''
    return helper.str_remove_dup_spaces(txt)


def pt_sec4_gas_flooding_injection_ratio_w_year(eo_field:str, year:int=None):
    year_txt = fill_year(year)
    prompt_gfir = (
        'From the above reference text, '
        f'if you can extract Gas flooding injection ratio for {eo_field}{year_txt}, '
        'what is it and its unit? '
        'If you were able to extracte the gas flooding injection ratio, '
        'please answer {Gas flooding injection ratio:value@Reference page and content}. '
        'If you were not able to extracte the gas flooding injection ratio, '
        'please answer {Gas flooding injection ratio:not_mentioned}. '
    )
    return prompt_gfir


def pt_sec4_sor_w_year(eo_field:str, year:int=None):
    ''' prompt of steam-to-oil ratio '''
    year_txt = fill_year(year)
    txt=f'''From the above reference text, if you can extract Steam-to-oil ratio (SOR) for {eo_field}{year_txt}, what is it?
    please answer {{Steam-to-oil ratio (SOR):value@Reference page and content}},Keep the reference text under 40 words,Otherwise, please answer {{Steam-to-oil ratio (SOR):not_mentioned}}Please use curly braces to enclose the answer.'''
    return helper.str_remove_dup_spaces(txt)


def pt_sec4_flood_gas(eo_field:str, year=None):
    flood_gas_types = ['1=Natural gas', "2=Nitrogen (N2)", '3=Carbon Dioxide (CO2)']
    q_flood_gas = what_type_of_a_for_field(eo_field,
                                           'Flood gas',
                                           types=flood_gas_types,
                                           what_question="Which number is it?")
    return q_flood_gas


def pt_sec4_f_of_co2(eo_field:str, year=None):
    qst = what_a_for_field(eo_field,
                        'Fraction of CO2 breaking through to producers',
                        what_question='what is it? ',
                        unit_question='what unit is it?')
    return qst


def pt_sec4_source_of_makeup_co2(eo_field:str, year=None):
    source_of_makeup_co2_types = ["1=Natural subsurface reservoir", "2=Anthropogenic"]
    q_source_of_makeup_co2 = what_type_of_a_for_field(eo_field,
                                                      'Source of makeup CO2',
                                                      types=source_of_makeup_co2_types,
                                                      what_question="Which number is it?")
    return q_source_of_makeup_co2


def pt_sec4_p_of_sequestration(eo_field:str, year=None):
    ''' prompt for Percentage of sequestration credit assigned to the oilfield '''
    qst = what_a_for_field(eo_field,
                          vars.VAR_SEC4_P_OF_SEQUESTRATION,
                          what_question='what is it? ',
                          unit_question='')
    return qst


def pt_sec4_f_of_fossil(eo_field:str, year=None):
    qst = what_a_for_field(eo_field,
                          vars.VAR_SEC4_F_OF_FOSSIL,
                          what_question='what is it? ',
                          unit_question='')
    return qst


def pt_sec4_f_of_ngas(eo_field:str, year=None):
    qst = what_a_for_field(eo_field,
                          vars.VAR_SEC4_F_OF_NGAS,
                          what_question='what is it? ',
                          unit_question='')
    return qst


def pt_sec4_f_of_water_reinjected(eo_field:str, year=None):
    '''
        prompt for Fraction of produced water reinjected
    '''
    return common_template(
        f'please determine the {vars.VAR_SEC4_F_OF_WATER_REINJECTED} that is reinjected for the {eo_field}.',
        eo_field=eo_field, field_name=vars.VAR_SEC4_F_OF_WATER_REINJECTED)


def pt_sec4_f_of_steam_cog(eo_field:str, year=None):
    qst = what_a_for_field(eo_field,
                          vars.VAR_SEC4_F_OF_STEAM_COG,
                          what_question='what is it? ',
                          unit_question='')
    return qst


def pt_sec4_f_of_steam_solar(eo_field:str, year=None):
    qst = what_a_for_field(eo_field,
                          vars.VAR_SEC4_F_OF_STEAM_SOLAR,
                          what_question='what is it? ',
                          unit_question='')
    return qst


def pt_sec4_production_practices(eo_field: str, year=None):
    ''' prompt for section 4: production practices '''
    q_pp = []

    pp_list=[pt_sec4_gor,
             pt_sec4_wor_w_year,
             pt_sec9_oil_production_bopd,
             pt_sec9_gas_production_mmscfd,
             pt_sec4_water_injection_ratio_w_year,
             pt_sec4_gas_lifting_injection_ratio_w_year,
             pt_sec4_gas_flooding_injection_ratio_w_year,
             pt_sec4_flood_gas,
             pt_sec4_f_of_co2,
             pt_sec4_source_of_makeup_co2,
             pt_sec4_p_of_sequestration,
             pt_sec4_sor_w_year,
             pt_sec4_f_of_fossil,
             pt_sec4_f_of_ngas,
             pt_sec4_f_of_water_reinjected,
             pt_sec4_f_of_steam_cog,
             pt_sec4_f_of_steam_solar,]

    for pp_key_promt_func in pp_list:
        pp_key_promt = pp_key_promt_func(eo_field, year)
        q_pp.append(pp_key_promt)

    ret = pt_combine_individuals(q_pp)
    return ret


def pt_sec5_heater_treater(eo_field: str, year=None):
    ''' prompt for section 5: heater/treater '''
    prompt = what_a_for_field(eo_field,
                            vars.VAR_SEC5_HEATER_TREATER,
                            what_question='what is it?')
    return prompt


def pt_sec5_stabilizer_column(eo_field: str, year=None):
    prompt = what_a_for_field(eo_field,
                            vars.VAR_SEC5_STABILIZER_COLUMN,
                            what_question='what is it?')
    return prompt


def pt_sec5_upgrader_type(eo_field: str, year=None):
    ''' prompt for upgrader type '''
    upgrader_types = ["0=None",
                      "1=Delayed coking",
                      "2=Hydroconversion",
                      "3=Combined hydroconversion and fluid coking", ]
    prompt = what_type_of_a_for_field(eo_field,
                                     'Upgrader type',
                                      types=upgrader_types,
                                      what_question="Which number is it?")
    return helper.str_remove_dup_spaces(prompt)


def pt_sec5_flaring_to_oil_ratio_w_year(eo_field: str, year=None):
    year_txt = fill_year(year)
    prompt = what_a_for_field(eo_field,
                            vars.VAR_SEC5_FLARING_TO_OIL_RATIO,
                            year_txt,
                            what_question='what is it?')
    return prompt


def pt_sec5_venting_fraction_w_year(eo_field: str, year=None):
    year_txt = fill_year(year)
    prompt = what_a_for_field(eo_field,
                            vars.VAR_SEC5_VENTING_FRACTION,
                            year_txt,
                            what_question='what is it?')
    return prompt


def pt_sec5_volume_fraction_of_diluent_w_year(eo_field: str, year=None):
    year_txt = fill_year(year)
    prompt = what_a_for_field(eo_field,
                            vars.VAR_SEC5_VOLUME_FRACTION_OF_DILUENT,
                            year_txt,
                            what_question='what is it?')
    return prompt


def pt_sec5_processing_practices(eo_field: str,year=None):
    # q_pp: question of processing practices
    q_pp = []
    q_pp.append(pt_sec5_heater_treater(eo_field))
    q_pp.append(pt_sec5_stabilizer_column(eo_field))
    q_pp.append(pt_sec5_upgrader_type(eo_field))
    q_pp.append(pt_sec5_flaring_to_oil_ratio_w_year(eo_field))
    q_pp.append(pt_sec5_venting_fraction_w_year(eo_field))
    q_pp.append(pt_sec5_volume_fraction_of_diluent_w_year(eo_field))
    ret = pt_combine_individuals(q_pp)
    return ret


def pt_field_year(eo_field: str):
    txt = (
        "According to the above text, "
        f"which specific years of oil/gas production of {eo_field} field is described in the above text? "
        "What is the oil/gas production of the field in the corresponding years? "
        "The output json must in the format of '{field: {year: oil/gas production}}'. "
        "If cannot extract the year, please answer '{field: null}'. "
        )
    return helper.str_remove_dup_spaces(txt)


def pt_field_year_all(field_names: List[str]):
    format_text = "Please answer questions and output the answer one by one. "

    question = [format_text]
    for field in field_names:
        question.append(pt_field_year(field))

    return '\n'.join(question)


def pt_sec6_excess_pressure(eo_field: str, year=None):
    prompt = (
        'From the above reference text, '
        f'extract the "value" and the "unit" of excess pressure in injector well in {eo_field}. '
        'Excess pressure in injector well equals to injector well\'s interface flowing pressure '
        'minus avg reservoir pressure. '
    )
    key = 'Excess pressure in injector well (injector well interface flowing pressure - avg res. pressure)'
    prompt += pt_extract_val_unit_part_2(key)
    return prompt


def pt_sec6_reservoir_permeability(eo_field: str, year=None):
    ''' reservoir permeability '''
    key = 'Reservoir permeability'
    fine_tune=('pay special attention to the unit, which are typically represented as "mD" or "μm2". '
               'Note that the result should be an actual field property and not a simulation result. ')
    return pt_extract_val_unit(key, eo_field, finetune=fine_tune)


def pt_sec6_reservoir_thickness(eo_field:str, year=None):
    ''' reservoir thickness '''
    key = "Reservoir thickness"
    finetune = (
        'Please note that reservior thickness is also called composite thickness. '
        #'Please also note that reservior thickness is NOT sand thickness. '
    )
    return pt_extract_val_unit(key, eo_field, finetune)


def pt_sec6_wellhead_pressure(eo_field: str, year=None):
    ''' wellhead pressure '''
    key = 'Wellhead pressure'
    return pt_extract_val_unit(key, eo_field)


def pt_sec6_wellhead_temperature(eo_field: str, year=None):
    ''' wellhead temperature '''
    key = 'Wellhead temperature'
    finetune = (
        f'{PROMPT_EXAMPLE_NO_RELATIVE_NUM}'
    )
    return pt_extract_val_unit(key, eo_field, finetune)


def pt_sec6_others(eo_field: str, year=None):
    '''
    prompt of section 6: others
    year is unused, but kept for compatibility
    '''
    p_po = []
    p_po.append(pt_sec6_excess_pressure(eo_field)) #1
    p_po.append(pt_sec6_reservoir_permeability(eo_field)) #2
    p_po.append(pt_sec6_reservoir_thickness(eo_field)) #3
    p_po.append(pt_sec6_wellhead_pressure(eo_field)) #4
    p_po.append(pt_sec6_wellhead_temperature(eo_field)) #5

    prompts = pt_combine_individuals(p_po)
    return prompts


# Whether to include example is decided per question
# inst: instruction
def pt_inst_llama2(ref: str, question: str):
    inst_llama2 = f'''[INST] <<SYS>>
                {SYS_MSG_EXTRACTOR}
                <</SYS>>
                ----- Start of the Reference Text -----
                {ref}
                ----- End of the Reference Text -----
                {question} [/INST]
                '''
    return inst_llama2


section_map = {
    "Production methods": pt_sec1_production_method,
    "Field properties": pt_sec2_field_properties,
    "Fluid properties": pt_sec3_fluid_properties,
    "Production practices": pt_sec4_production_practices,
    "Processing practices": pt_sec5_processing_practices,
    "Others": pt_sec6_others,
}

pt_attribute_1to1_map =  {
    # Production methods (9 attr)
    vars.VAR_SEC1_DOWNHOLE_PUMP: pt_sec1_downhole_pump,
    vars.VAR_SEC1_WATER_REINJECTION: pt_sec1_water_reinjection,
    vars.VAR_SEC1_NATURAL_GAS_REINJECTION: pt_sec1_natural_gas_reinjection,
    vars.VAR_SEC1_WATER_FLOODING: pt_sec1_water_flooding,
    vars.VAR_SEC1_GAS_LIFTING: pt_sec1_gas_lifting,
    vars.VAR_SEC1_GAS_FLOODING: pt_sec1_gas_flooding,
    vars.VAR_SEC1_STEAM_FLOODING: pt_sec1_steam_flooding,
    vars.VAR_SEC1_OIL_SANDS_MINE_I: pt_sec1_oil_sands_mine_i,
    vars.VAR_SEC1_OIL_SANDS_MINE_NI: pt_sec1_oil_sands_mine_ni,

    # field properties (13 attr)
    vars.VAR_SEC2_FIELD_LOCATION: pt_sec2_field_location,
    vars.VAR_SEC2_FIELD_NAME: pt_sec2_field_name,
    vars.VAR_SEC2_FIELD_AGE: pt_sec2_field_age_w_year_individual,
    vars.VAR_SEC2_FIELD_DEPTH: pt_sec2_field_depth,
    vars.VAR_SEC2_PRODUCTION_VOLUME: pt_sec2_production_volume_w_year,
    vars.VAR_SEC2_NUM_OF_PRODUCING_WELLS: pt_sec2_num_of_producing_wells_w_year,
    vars.VAR_SEC2_NUM_OF_WATER_INJECTING_WELLS: pt_sec2_num_of_water_injecting_wells_w_year,
    vars.VAR_SEC2_PRODUCTION_TUBING_DIAMETER: pt_sec2_production_tubing_diameter,
    vars.VAR_SEC2_INJECTOR_TUBING_DIAMETER: pt_sec2_injector_tubing_diameter,
    vars.VAR_SEC2_BOTTOMHOLE_PRESSURE: pt_sec2_bottomhole_pressure,
    vars.VAR_SEC2_RESERVOIR_PRESSURE: pt_sec2_reservoir_pressure,
    vars.VAR_SEC2_RESERVOIR_TEMPERATURE: pt_sec2_reservoir_temperature,
    vars.VAR_SEC2_OFFSHORE: pt_sec2_offshore,

    # section 3 (8 attr)
    vars.VAR_SEC3_API_GRAVITY: pt_sec3_api_gravity,
    vars.VAR_SEC3_N2: pt_sec3_n2,
    vars.VAR_SEC3_CO2: pt_sec3_co2,
    vars.VAR_SEC3_C1: pt_sec3_c1,
    vars.VAR_SEC3_C2: pt_sec3_c2,
    vars.VAR_SEC3_C3: pt_sec3_c3,
    vars.VAR_SEC3_C4_PLUS: pt_sec3_c4_plus,
    vars.VAR_SEC3_H2S: pt_sec3_h2s,

    # section 4 (15 attr)
    vars.VAR_SEC4_GOR: pt_sec4_gor,
    vars.VAR_SEC4_WOR: pt_sec4_wor_w_year,
    vars.VAR_SEC9_OIL_PRODUCTION_BOPD: pt_sec9_oil_production_bopd,
    vars.VAR_SEC9_Gas_Production_Mmscfd: pt_sec9_gas_production_mmscfd,
    vars.VAR_SEC4_WATER_INJECTION_RATIO: pt_sec4_water_injection_ratio_w_year,
    vars.VAR_SEC4_GAS_LIFTING_INJECTION_RATIO:
                                pt_sec4_gas_lifting_injection_ratio_w_year,
    vars.VAR_SEC4_GAS_FLOODING_INJECTION_RATIO:
                                pt_sec4_gas_flooding_injection_ratio_w_year,
    vars.VAR_SEC4_FLOOD_GAS: pt_sec4_flood_gas,
    vars.VAR_SEC4_F_OF_CO2: pt_sec4_f_of_co2,
    vars.VAR_SEC4_SOURCE_OF_MAKEUP_CO2: pt_sec4_source_of_makeup_co2,
    vars.VAR_SEC4_P_OF_SEQUESTRATION: pt_sec4_p_of_sequestration,
    vars.VAR_SEC4_SOR: pt_sec4_sor_w_year,
    vars.VAR_SEC4_F_OF_FOSSIL: pt_sec4_f_of_fossil,
    vars.VAR_SEC4_F_OF_NGAS: pt_sec4_f_of_ngas,
    vars.VAR_SEC4_F_OF_WATER_REINJECTED: pt_sec4_f_of_water_reinjected,
    vars.VAR_SEC4_F_OF_STEAM_COG: pt_sec4_f_of_steam_cog,
    vars.VAR_SEC4_F_OF_STEAM_SOLAR: pt_sec4_f_of_steam_solar,

    # section 5 (6 attr)
    vars.VAR_SEC5_HEATER_TREATER: pt_sec5_heater_treater,
    vars.VAR_SEC5_STABILIZER_COLUMN: pt_sec5_stabilizer_column,
    vars.VAR_SEC5_UPGRADER_TYPE: pt_sec5_upgrader_type,
    vars.VAR_SEC5_FLARING_TO_OIL_RATIO: pt_sec5_flaring_to_oil_ratio_w_year,
    vars.VAR_SEC5_VENTING_FRACTION: pt_sec5_venting_fraction_w_year,
    vars.VAR_SEC5_VOLUME_FRACTION_OF_DILUENT: pt_sec5_volume_fraction_of_diluent_w_year,

    # Others (5 attr)
    vars.VAR_SEC6_EXCESS_PRESSURE: pt_sec6_excess_pressure,
    vars.VAR_SEC6_RESERVOIR_PERMEABILITY: pt_sec6_reservoir_permeability,
    vars.VAR_SEC6_RESERVOIR_THICKNESS: pt_sec6_reservoir_thickness,
    vars.VAR_SEC6_WELLHEAD_PRESSURE: pt_sec6_wellhead_pressure,
    vars.VAR_SEC6_WELLHEAD_TEMPERATURE: pt_sec6_wellhead_temperature,
}

def pt_dynamic_map(eo_field: str, year=None):
    '''
    A average of our current prompt is 300 tokens.
    We combine three questions together to make a prompt rougly 1K tokens.
    This is to use for small context window model, such as llama2. (4K window)
    There are few restrictions for the prompt:
    1. Since we process the list in order, three longer prompts will result in
    a much longer prompt, such as len(# of wells) is more than 400 tokens.
    2. It won't make much difference with individual questions if only three
    are combined.
    3. We do not put it into a real run. This function is only used for
    showing a possible way to group prompts.
    '''
    dynamic_map = {}
    lst_attribute_prompt = []
    for func in pt_attribute_1to1_map.values():
        prompt = func(eo_field, year)
        lst_attribute_prompt.append(prompt)

    for i in range(0, len(lst_attribute_prompt), 3):
        # python will handle the index out of range error
        # and return properly sliced list
        lst_prompt = lst_attribute_prompt[i:i+3]
        combined_prompts = pt_combine_individuals(lst_prompt)
        dynamic_map[f'group_{i // 3 + 1}'] = combined_prompts

    return dynamic_map

if __name__ == '__main__':
    # section_map=pt_methods_and_properties_i2()
    # for key , val in section_map.items():
    #     print(key,val("Okha"))
    # lst = pt_field_properties_i("Okha")
    # print(lst)
    #print(pt_sec5_processing_practices("smiley buffalo",2023))
    ret = pt_dynamic_map("Okha")
    print(ret)
