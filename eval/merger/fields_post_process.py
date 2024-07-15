import operator
import pandas as pd
from lib.my_logger import logger
from typing import List
from eval.singleton import Singleton
from eval.parser.parser_response import ParserResponse

_fields_handler = {}

#
Field_depth = 'Field depth'
Reservior_thickness = 'Reservoir thickness'
GOR = 'Gas-to-oil ratio (GOR)'
Gas_Production_Mmscfd = 'Gas_Production_Mmscfd'
Oil_Production_BOPD = 'Oil_Production_BOPD'


def fields_handler(*args):
    """
    Decorator that registers a function as a handler for a specific field in the dictionary.
    """

    def _handler(func):
        _fields_handler[args] = func

    return _handler


class FieldsProcess(metaclass=Singleton):

    def fields_post_process(self, responses: List[ParserResponse]):
        '''
        Perform post-processing on specified fields. find the index corresponding to the field
        '''
        fields = ((Field_depth, Reservior_thickness), (GOR, Gas_Production_Mmscfd, Oil_Production_BOPD))

        for field in fields:
            fields_index = []
            for f in field:
                for idx in range(len(responses)):
                    if responses[idx].variable.name == f:
                        fields_index.append(idx)

            try:
                _fields_handler.get(field)(self, responses, fields_index)
            except:
                logger.error(f'{fields} are not registered')

    @fields_handler(Field_depth, Reservior_thickness)
    def field_depth_post_process(self, responses: List[ParserResponse], fields_index: List[int]
                                 ):
        '''
        depth = depth + thickness/2
        '''
        try:
            thickness_half = float(responses[fields_index[1]].result.data.value) / 2
            if not pd.isna(thickness_half):
                responses[fields_index[0]].result.data.value = round(operator.add(
                    float(responses[fields_index[0]].result.data.value),
                    thickness_half), 2)
        except:
            pass

    @fields_handler(GOR, Gas_Production_Mmscfd, Oil_Production_BOPD)
    def gor_post_process(self, responses: List[ParserResponse], fields_index: List[int]
                         ):
        '''
        If GOR already has a value, use that; otherwise
        gor = Gas_Production_Mmscfd*1000000/Oil_Production_BOPD
        '''
        try:
            responses[fields_index[0]].result.data.value = round(operator.truediv(
                float(responses[fields_index[1]].result.data.value) * 10 ** 6,
                float(responses[fields_index[2]].result.data.value)), 2
            ) if pd.isna(responses[fields_index[0]].result.data.value) else responses[fields_index[0]].result.data.value
        except:
            pass