from eval.parser.parser_response import ParserResponse
from eval.parser.parser_result import ParserSuccessResult, ParserData
import schema.variables as variables
from eval.merger.fields_post_process import FieldsProcess
import unittest
import numpy as np


# Assuming ParserResponse has attributes like 'variable' and 'result' as used in the function
# and Result has an attribute 'data' which in turn has a 'value' attribute.


class TestFieldsPostProcess(unittest.TestCase):

    def test_fields_post_process(self):
        responses = [
            ParserResponse(variable=variables.Variable(name='Field 1 depth', value_parser=None, merger=None),
                           result=ParserSuccessResult(data=ParserData(value=10)),
                           field='Field depth', record='', section='', raw_text=''
                           ),
            ParserResponse(variable=variables.Variable(name='Field depth', value_parser=None, merger=None),
                           result=ParserSuccessResult(data=ParserData(value=10)),
                           field='Field depth', record='', section='', raw_text=''
                           ),
            ParserResponse(variable=variables.Variable(name='Reservoir thickness', value_parser=None, merger=None),
                           result=ParserSuccessResult(data=ParserData(value='20')),
                           field='Reservoir thickness', record='', section='', raw_text='')]

        # Act
        FieldsProcess().fields_post_process(responses)

        # Assert
        assert float(responses[1].result.data.value) == float(20)
        # assert responses[0].result.data.value == np.nan

    def test_gor_post_process(self):
        responses = [
            ParserResponse(variable=variables.Variable(name='Field 1 depth', value_parser=None, merger=None),
                           result=ParserSuccessResult(data=ParserData(value=10)),
                           field='Field depth', record='', section='', raw_text=''
                           ),
            ParserResponse(variable=variables.Variable(name='Field depth', value_parser=None, merger=None),
                           result=ParserSuccessResult(data=ParserData(value=10)),
                           field='Field depth', record='', section='', raw_text=''
                           ),
            ParserResponse(variable=variables.Variable(name='Gas-to-oil ratio (GOR)', value_parser=None, merger=None),
                           result=ParserSuccessResult(data=ParserData(value=np.nan)),
                           field='Gas-to-oil ratio (GOR)', record='', section='', raw_text=''
                           ),
            ParserResponse(variable=variables.Variable(name='Gas_Production_Mmscfd', value_parser=None, merger=None),
                           result=ParserSuccessResult(data=ParserData(value=10)),
                           field='Gas_Production_Mmscfd', record='', section='', raw_text=''
                           ),
            ParserResponse(variable=variables.Variable(name='Oil_Production_BOPD', value_parser=None, merger=None),
                           result=ParserSuccessResult(data=ParserData(value='20')),
                           field='Oil_Production_BOPD', record='', section='', raw_text='')]

        # Act
        FieldsProcess().fields_post_process(responses)

        # Assert
        # assert float(responses[2].result.data.value) == float(10)
        assert float(responses[1].result.data.value) == float(10)
        assert float(responses[2].result.data.value) == float(500000)
        # assert responses[0].result.data.value == np.nan

    def test_gor_nan_post_process(self):
        responses = [
            ParserResponse(variable=variables.Variable(name='Field 1 depth', value_parser=None, merger=None),
                           result=ParserSuccessResult(data=ParserData(value=10)),
                           field='Field depth', record='', section='', raw_text=''
                           ),
            ParserResponse(variable=variables.Variable(name='Field depth', value_parser=None, merger=None),
                           result=ParserSuccessResult(data=ParserData(value=10)),
                           field='Field depth', record='', section='', raw_text=''
                           ),
            ParserResponse(variable=variables.Variable(name='Gas-to-oil ratio (GOR)', value_parser=None, merger=None),
                           result=ParserSuccessResult(data=ParserData(value=np.nan)),
                           field='Gas-to-oil ratio (GOR)', record='', section='', raw_text=''
                           ),
            ParserResponse(variable=variables.Variable(name='Gas_Production_Mmscfd', value_parser=None, merger=None),
                           result=ParserSuccessResult(data=ParserData(value=np.nan)),
                           field='Gas_Production_Mmscfd', record='', section='', raw_text=''
                           ),
            ParserResponse(variable=variables.Variable(name='Oil_Production_BOPD', value_parser=None, merger=None),
                           result=ParserSuccessResult(data=ParserData(value=33)),
                           field='Oil_Production_BOPD', record='', section='', raw_text='')]

        # Act
        FieldsProcess().fields_post_process(responses)
        # Assert
        assert float(responses[1].result.data.value) == float(10)
        assert np.isnan(responses[2].result.data.value)
