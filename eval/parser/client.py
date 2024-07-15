from __future__ import annotations

from typing import List, Optional
import re

from config import UNKNOWN_TEXT, SPLET_KEY_VALUE_CHAR
from lib.my_logger import logger
from eval.parser.parser_result import SUCCESS, ERROR, ParserErrorResult, ParserData, ParserSuccessResult
from eval.parser.parser_text import ParserText
from schema.variables import Variable, get_variable, variable_list
from eval.exception import ParserException, RESPONSE_FORMAT_ERROR, RESPONSE_COLON_ERROR, RESPONSE_MISSING_VARIABLE_ERROR
import eval.standardizer.standarizer as standardizer
from .parser_response import ParserResponse
from eval.parser.parser_utils import SPLIT_ERROR_CHAR


class ParserClient:
    def __init__(
            self, model: str,
            field_name: str,
            variables: Optional[List[str]] = None,
            section: Optional[str] = None,
            reference: str = ''
    ):
        self.model = model
        self.field_name = field_name

        self.unparsed_responses: List[ParserResponse] = []
        self.failed_responses: List[ParserResponse] = []
        self.succeed_responses: List[ParserResponse] = []

        self.reference: str = reference
        self.section: str = section
        self.variables: List[Variable] = get_variable(section=self.section, var_names=variables,
                                                      ignore=['Field name'], only_gt=False)
        self.split_count = 1

        self.standardizer = standardizer.Standardizer(self.model, self.reference)

    def parse(self, llm_response: str):

        logger.info(f"Begin parsing multiple llm outputs for field: {self.field_name}, section: {self.section}")

        self.parse_llm_response(llm_response)
        self.re_parse()

        if len(self.failed_responses) != 0:
            logger.warning(f"records cannot be reformatted by standardizer: {self.failed_responses}")

        logger.info(
            f"""
            Finished to parse {self.model} outputs for field: {self.field_name}, section: {self.section},
            {len(self.succeed_responses)} succeed, {len(self.failed_responses)} failed, {len(self.unparsed_responses)} 
            cannot parse.
            """
        )
        self.complete_missing_responses()

    def parse_llm_response(self, llm_response: str):
        """
        :param llm_response: AI Model output for one question section of one block of paper
        """

        if len(self.variables) == 0:
            raise KeyError(f'Section {self.section} not in variable map')

        records = re.findall(r'{(.*?)}', llm_response)

        if len(self.variables) != len(records):
            message = f"section '{self.section}' require {len(self.variables)} records, " \
                      f"but {len(records)} are extracted from {self.model}"
            status = ERROR
            result = ParserErrorResult(
                data=ParserData(status=status),
                feedback=self.standardizer.handle_re_extract_llm,
                error=ParserException(
                    RESPONSE_FORMAT_ERROR,
                    {"exception": message, "content": llm_response, "records": records},
                    cls_name=type(self).__name__
                ),
                status=status,
            )
            response = ParserResponse(self.field_name, llm_response, self.section, '', None, result)
            self.unparsed_responses.append(response)
            logger.error(result.error.payload)

        # print(self.failed_response)
        for record in records:
            self.parse_record(record, self.variables)

    def parse_record(self, record: str, variables: List[Variable]):
        ''' Parse one record in llm response. '''
        # make sure there is no new line in record specially in @reference content
        record = record.strip().replace('\r\n', ' ').replace('\n', ' ')
        if SPLET_KEY_VALUE_CHAR not in record:
            message = f"record {record} does not seperated by ':'"
            status = ERROR
            result = ParserErrorResult(
                data=ParserData(status=status),
                feedback=self.standardizer.handle_reformat_colon,
                error=ParserException(
                    RESPONSE_COLON_ERROR,
                    {"exception": message, "content": record},
                    cls_name=type(self).__name__
                ),
                status=status,
            )
            logger.error(result.error.payload)
            self.unparsed_responses.append(ParserResponse(self.field_name, record, self.section, '', None, result))
        else:
            raw_key, raw_value = record.strip().split(SPLET_KEY_VALUE_CHAR, self.split_count)

            if parsed_key := self.parse_key(record, raw_key):
                self.parse_value(record, parsed_key, raw_value, variables)

    def parse_key(self, raw_record: str, raw_key_text: str,) -> Optional[str]:
        """
        A record is a string text with form "key:value@reference".
        :param raw_record: unprocessed string rext for record,
        :param raw_key_text: unprocessed string text for variable key,

        Return: parsed result ParseResult.
        """

        raw_key_text = raw_key_text.strip()
        key_result = ParserText().parse(raw_key_text)
        if key_result.status == ERROR:
            key_result.feedback = self.standardizer.handle_re_extract_llm,
            self.unparsed_responses.append(ParserResponse(self.field_name, raw_record, self.section, '', None, key_result))
            logger.Error(f"'{raw_key_text}' failed to be parsed to text. Got exception: {key_result.error}")
            return
        return key_result.data.value

    def parse_value(self, raw_record: str, key: str, raw_value_text: str, variables: List[Variable] = None):
        """
        A record is a string text with form "key:value@reference".
        :param raw_record: unprocessed string rext for record,
        :param key: unprocessed string text for variable key,
        :param raw_value_text: unprocessed string text for variable value,
        :param variables: The variable list that the key may in.
        """
        raw_value_text = raw_value_text.strip()

        variable = self.find_variable(key, variables)

        if not variable:
            failed_vars = self.find_missing_variable()
            for var in failed_vars:
                message = f"Not find {key} in {variables}."
                status = ERROR
                result = ParserErrorResult(
                    data=ParserData(status=status),
                    feedback=self.standardizer.handle_re_extract_llm,
                    error=ParserException(
                        RESPONSE_MISSING_VARIABLE_ERROR,
                        {"exception": message, "content": raw_value_text, "records": raw_record},
                        cls_name=type(self).__name__
                    ),
                    status=status,
                )
                response = ParserResponse(self.field_name, raw_record, self.section, raw_record, var, result)
                self.unparsed_responses.append(response)
                logger.error(result.error.payload)
        else:
            result = variable.value_parser().parse(raw_value_text, key=variable.name, unit=variable.unit)
            response = ParserResponse(self.field_name, raw_record, self.section, raw_value_text, variable, result)

            if result.status == SUCCESS:
                self.succeed_responses.append(response)
            elif result.status == ERROR:
                self.failed_responses.append(response)
            else:
                raise ValueError(f"parsed status {result.status} is not valid, \
                    the value for parsed result status is 'error' or 'success'")

    def re_parse(self):
        resp_list = self.failed_responses + self.unparsed_responses
        while len(resp_list) > 0:
            resp = resp_list.pop()
            if resp.variable is None:
                vars = self.find_missing_variable()
                if len(vars) > 0:
                    resp.variable = vars[0]

            if resp.result.feedback is not None:
                logger.info(f"Standardizer Process: {self.field_name}, {self.section}, {resp.variable}: {resp.record}")
                llm_response = resp.result.feedback(self.field_name, self.section, resp.record, resp.variable)
                records = re.findall(r'{(.*?)}', llm_response)

                if resp.variable is None:
                    variables = self.variables
                else:
                    variables = [resp.variable]
                for record in records:
                    self.parse_record(record, variables)

    def find_missing_variable(self) -> List[Variable]:
        parsed_keys = [resp.variable.name for resp in self.succeed_responses + self.failed_responses]

        result = []

        # 'Field name' variable is ignored, here need to add back.
        if self.section == 'Field properties':
            variables = get_variable(section=self.section)
        else:
            variables = self.variables

        for var in variables:
            if var.name not in parsed_keys:
                result.append(var)
        return result

    def find_variable(self, parsed_key: str, variables: List[Variable] = None) -> Optional[Variable]:
        if not variables:
            variables = self.variables

        for var in variables:
            if var.name.lower() == parsed_key.lower():
                return var

    def find_response(self, parsed_key: str, where: str) -> List[ParserResponse]:
        if where == 'failed':
            responses = self.failed_responses
        elif where == 'unparsed':
            responses = self.unparsed_responses
        else:
            responses = self.succeed_responses

        rslts = []
        for resp in responses:
            if resp.variable is not None and resp.variable.name == parsed_key:
                rslts.append(resp)

        return rslts

    def complete_missing_responses(self):
        missing_variables = self.find_missing_variable()
        for var in missing_variables:
            if var.name == 'Field name':
                data = ParserData(value=self.field_name, unit='', ref='', status=SUCCESS)
                message = ''
                raw_text = self.field_name
                result = ParserSuccessResult(data, status=data.status)
            else:
                unparsed_resps = self.find_response(var.name, where='unparsed')
                message = SPLIT_ERROR_CHAR.join([resp.record for resp in unparsed_resps])
                raw_text = UNKNOWN_TEXT
                data = ParserData(status=ERROR)

                exception = ParserException(
                    code=RESPONSE_MISSING_VARIABLE_ERROR,
                    cls_name=type(self).__name__,
                    payload=message
                )
                result = ParserErrorResult(data, error=exception, status=ERROR)

            response = ParserResponse(
                field=self.field_name,
                section=self.section,
                record='',
                raw_text=raw_text,
                variable=var,
                result=result,
            )
            self.failed_responses.append(response)

    def show_responses(self):
        for resp in self.succeed_responses:
            print(f"Var: {resp.variable.name}, Value: {resp.result.data}")

    def show_failed_responses(self):
        for resp in self.failed_responses:
            print(f"Var: {resp.variable.name}, Value: {resp.result.data}")

    def get_responses(self) -> List[ParserResponse]:
        key_order = [var.name for var in variable_list]
        responses = sorted(self.succeed_responses + self.failed_responses, key=lambda x: key_order.index(x.variable.name))
        return responses
