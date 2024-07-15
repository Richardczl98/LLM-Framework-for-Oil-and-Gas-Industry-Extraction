from extractor import chat_llm

from model.prompt_template import pt_standardize_text, section_map, pt_attribute_1to1_map
from schema.variables import Variable
from lib.my_logger import logger


class Standardizer:
    def __init__(self, model: str = 'gpt-4', reference: str = ''):
        self.model: str = model
        self.reference: str = reference

    def handle_re_extract_llm(self, field: str, section: str = None, record: str = None, variable: Variable = None) -> str:
        if variable:
            question = pt_attribute_1to1_map[variable.name](field)
        elif section:
            question = section_map[section](field)
        else:
            logger.exception("No section and variable provided, give up standardize.")
            return ''

        return chat_llm.ask_extractor_question_from_ref(self.model, self.reference, question)

    def handle_reformat_colon(self, field: str, section: str, record: str, variable: Variable) -> str:
        question = pt_standardize_text(record)
        return chat_llm.ask_formatter_instruct_and_ref(question, model=self.model)

