# -*- coding: utf-8 -*-
# Author: Anjing Wang
# Date: Jan-04-2024

"""
Enumerate fields from a paper
"""
import os
import sys
import enum

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')
from extractor.chat_llm import ask_extractor_question_from_ref
from converter.zip2txt import zip_to_text
from model.models import MDL_GPT_4_T
from lib.my_logger import logger

STR_SUMMARIZE_BEGINNING = (
    'The above reference is an academic paper about oil or gas fields. '
    'Please read it through and summarize what oil fields (or gas fields) '
    'are mianly discussed in the above paper. '
)

STR_SUMMARIZE_ENDING = (
    'List oil or gas fields only, but not basins as basins might distract your reasoning. '
    'Only list the fileds that some of its properties '
    'such as oil production volume, Reservoir pressure or other properties, are discussed. '
    'If only a field\'s location is mentioned, but no other properties, exclude it. '
    'Our goal is to list the fields then extract its properties later. '
    'So we do not want to list a field, but nothing about it is mentioned in the paper. '
    'For each field, please provide the field name and '
    'what aspects of it are discussed in the paper.'
)


class PaperTypeEnum(enum.Enum):
    UNKNOWN = 'Unknown'
    FOCUSED_SURVEY_PAPER = 'Focused Survey Paper'
    BROAD_SURVEY_PAPER = 'Broad Survey Paper'


class EnumFields:
    ''' enumerate fields from a paper '''
    def __init__(self, strict=False):
        self.paper_full_path = None # e.g. /home/data/spe-210009-ms.pdf
        self.paper_name = None   # e.g. spe-210009-ms no extension
        self.zip_name = None
        self.pdf_name = None
        self.paper_text = None
        self.type_reasoning = None
        self.type = None
        self.summary = None
        self.summary_excluded = None
        # text of fields, e.g. "field1, field2, field3"
        self.fields_text = None
        # python list of fields
        self.field_list = None
        self.strict = strict

        # In the current dataset, most papers are focused survey papers
        # e.g. spe-210009-ms
        self.type_focused = PaperTypeEnum.FOCUSED_SURVEY_PAPER.value
        # e.g. 'spe-115712-ms, spe-28002-ms'
        self.type_broad = PaperTypeEnum.BROAD_SURVEY_PAPER.value
        self.type_unknown = PaperTypeEnum.UNKNOWN.value

        self._sys_msg_summarize = (
            'You are an AI assitant to summarize acedemic papers. '
            'Use your best knowledge, and follow the instructions in the prompt properly. '
        )
        self._prompt_summarize_focused = (
            f'{STR_SUMMARIZE_BEGINNING}'
            'Those oil or gas fields are firstly mentioned or brought up '
            'in the paper\'s title, abstract or introduction section. '
            'But if a field is only mentioned in or before the introduction section, '
            'without more details about its properties in the rest of the paper, '
            'please ignore it and do not count it in. '
            'Please also ignore any fields that firstly mentioned after the introduction section.'
            'We only would like to list the fields that the paper focuses on, '
            'not blindly list all the fileds mentioned in the paper. '
            f'{STR_SUMMARIZE_ENDING}'
        )
        self._prompt_summarize_broad = (
            f'{STR_SUMMARIZE_BEGINNING}'
            'Firstly, consider the fields that are firstly mentioned or brought up '
            'in the paper\'s title, abstract or introduction section. '
            'Secondly, consider the fields that are firstly brought up '
            'beyond the introduction section. '
            'Ignore any fields that firstly brought up in the reference or appendix section. '
            f'{STR_SUMMARIZE_ENDING}'
        )

        self._sys_msg_enumerate = (
            'You are an AI assitant to enumerate fields. '
            'Follow the instructions in the prompt properly. '
        )
        self._prompt_enumerate = (
            # spe-9478-pa: might have duplicate of "Hewitt Unit" and "Hewitt"
            # spe-175587-ms: have feild name "xx, block A", colon as the seperator
            'Please list oil fields (or gas fields) that are discussed in the above text. '
            'If there is only one field, please only list the field name. '
            'If there are multiple fields, please seperate the field names by a semicolon, '
            'such as "field1; field2; field3". '
            'Do not put a period at the end of the field name. '
            'Do not give any reasoning if any fields can be extracted. '
            'If there is no field mentioned, please answer none. '
            'Then give a reasoning after a new line if the answer is "none". '
            'Output the word "none" only, no quotes, no period after it.'
            'Also, please keep in mind that usually you do not need '
            'include Field in the filed name. '
            'For example, if the reference text mentions '
            'Tiguino, answer Tiguino instead of Tiguino Field. '
            'However, when excluding Field makes the field name ambiguous, '
            'keep Field. For example, if the reference text mentions '
            'North Field, you need to extract North Field instead of North, '
            'since North can mean too many things.'
            'Make sure you do not duplicate any field names. '
            'It\'s a good practice to always keep "Unit" if "Unit" is part '
            'of the field name. For example, always use "Hewitt Unit" '
            'instead of "Hewitt". By doing this, you avoid potential duplications '
            'of "Hewitt Unit" and "Hewitt".'
        )

        self._sys_msg_identify_type = (
            'You serve as an AI assistant specialized '
            'in categorizing academic papers into specific types. '
            'Ensure to follow the instructions in the prompt accurately.'
        )
        self._prompt_identify_type = (
            'The above reference is an academic paper about oil or gas fields. '
            'Please read it through and determine its type, '
            'classifying it as either: \n'
            f'(1) {self.type_focused}: This type of papers surveys fields '
            'in a specific country or region, concentrating on '
            'a limited number of fields. These fields are initially mentioned '
            'in the paper\'s title, abstract, or introduction. \n'
            f'(2) {self.type_broad}: This type of papers survey numerous fields '
            'in a country, multiple countries, or a specific region. '
            'New fields are continuously introduced and discussed '
            'beyond the abstract and introduction. \n'
            'Please respond starting with only the style name, '
            'and do not put anything before the style name. '
            'Then, provide the reasoning for your choice.'
        )

    def set_paper(self, paper_name):
        ''' set the paper name '''
        self.paper_full_path = None
        self.paper_name = None
        self.zip_name = None
        self.pdf_name = None
        self.paper_text = None
        self.type_reasoning = None
        self.type = None
        self.summary = None
        self.summary_excluded = None
        self.fields_text = None
        self.field_list = None

        if '/' in paper_name:
            self.paper_full_path = paper_name
            self.paper_name = paper_name.split('/')[-1]
        else:
            self.paper_name = paper_name

        if '.pdf' in self.paper_name or \
            '.zip' in self.paper_name or \
            '.txt' in self.paper_name:
            self.paper_name = self.paper_name[:-4]

        self.pdf_name = self.paper_name + '.pdf'
        self.zip_name = self.paper_name + '.zip'
        return

    def load_text(self):
        '''load text from zip'''
        if self.paper_name is None:
            return False

        # directly load the text if it is a .txt file
        if self.paper_full_path.endswith('.txt'):
            with open(self.paper_full_path, 'r', encoding='utf-8') as f:
                self.paper_text = f.read()
            return self.paper_text

        # this is out pdf conversion directory structure
        # find the zip file and convert to txt
        if 'tst' in self.paper_full_path:
            full_path_zip = this_file_path + \
                '/../data/tst/spe/zips/' + self.zip_name
        else:
            full_path_zip = this_file_path + \
                '/../data/zips/' + self.zip_name
        # if we do not have the zip file
        if not os.path.exists(full_path_zip):
            return False

        self.paper_text = zip_to_text(full_path_zip)
        return self.paper_text

    def identify_type(self):
        '''identify_type the text'''
        if self.paper_name is None:
            return False

        if self.type is not None:
            return self.type

        if self.paper_text is None:
            self.load_text()
        self.type_reasoning = ask_extractor_question_from_ref(model = MDL_GPT_4_T,
                                                           ref = self.paper_text,
                                                           question = self._prompt_identify_type,
                                                           sys_msg = self._sys_msg_identify_type)
        logger.debug(self.type_reasoning)
        if self.type_reasoning.strip().lower().startswith(self.type_focused.lower()):
            self.type = self.type_focused
        elif self.type_reasoning.strip().lower().startswith(self.type_broad.lower()):
            self.type = self.type_broad
        else:
            self.type = self.type_unknown

        logger.debug(self.type)
        return self.type

    def summarize(self):
        '''summarize the text'''
        if self.paper_name is None:
            return False

        if self.summary is not None:
            return self.summary

        if self.type is None:
            self.identify_type()

        if self.type == self.type_broad:
            self.summary = ask_extractor_question_from_ref(
                                model = MDL_GPT_4_T,
                                ref = self.paper_text,
                                question = self._prompt_summarize_broad,
                                sys_msg = self._sys_msg_summarize)
            logger.debug(self.summary)
        else:
            self.summary = ask_extractor_question_from_ref(
                                    model = MDL_GPT_4_T,
                                    ref = self.paper_text,
                                    question = self._prompt_summarize_focused,
                                    sys_msg = self._sys_msg_summarize)
            logger.debug(self.summary)
            if self.strict is True:
                prompt_summarize_excluded = (
                    'The current of the summary of the paper is as follows: \n'
                    f'{self.summary} \n'
                    'Look at the summary one more time, list those fields '
                    'that are not mentioned in the original reference paper '
                    'after the introduction section. '
                    'None of their properties are discussed after the introduction. '
                    'List those fields, and give the reasoning. '
                    'If every field is mentioned and discussed after the introduction, '
                    'then list "None".'
                )
                self.summary_excluded = ask_extractor_question_from_ref(
                                        model = MDL_GPT_4_T,
                                        ref = self.paper_text,
                                        question = prompt_summarize_excluded,
                                        sys_msg = self._sys_msg_summarize)

                logger.debug(self.summary_excluded)

        return self.summary

    def enumerate(self):
        '''enumerate the fields'''
        if self.paper_name is None:
            return False

        if self.fields_text is not None:
            return self.fields_text

        if self.summary is None:
            self.summarize()

        ref_summary = self.summary
        if self.summary_excluded is not None:
            ref_summary = self.summary_excluded
        self.fields_text = ask_extractor_question_from_ref(model = MDL_GPT_4_T,
                                                           ref = ref_summary,
                                                           question = self._prompt_enumerate,
                                                           sys_msg = self._sys_msg_enumerate)
        logger.debug(self.fields_text)
        return self.fields_text

    def get_field_list(self):
        '''return a list of fields'''
        if self.paper_name is None:
            return False

        if self.field_list is not None:
            return self.field_list

        if self.fields_text is None:
            self.enumerate()

        if self.fields_text.lower().strip().startswith('none'):
            self.field_list = []
        else:
            # Chatgpt might return something weird like 'Daqing Field\n\nnone'
            # so we always take the first line just in case
            first_line = self.fields_text.split('\n', 1)[0]
            self.field_list = [item.strip() for item in first_line.split(';')]

        logger.debug(self.field_list)
        return self.field_list

if __name__ == '__main__':
    ef = EnumFields()
    ef.set_paper('spe-115712-ms')
    # # ['Buracica', 'Carmópolis', 'Canto do Amaro', 'Jubarte', 'Marlim', 'Lula', 'Mero']
    print(ef.get_field_list())
    # print(ef.summarize())
