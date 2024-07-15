import os
import sys

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')
from lib.my_logger import logger
from lib import helper
import model.prompt_template as pt


# *****************************README*************************************
# In order to fix the output format of the model, please refer to the following format
# {key:value unit/Reference page and content}
# ******************************************************************
# example
"""
{Downhole pump:not_mentioned}
{Water reinjection:not_mentioned}
{Natural gas reinjection:not_mentioned}
{Water flooding:not_mentioned}
{Gas lifting:not_mentioned}
{Gas flooding:not_mentioned}
{Steam flooding:mentioned/Page 6, "Steam flooding3,5,24,29 and hot water flooding5,26......}
{Oil sands mine (integrated with upgrader):not_mentioned}
{Oil sands mine (non-integrated with upgrader):not_mentioned}
"""


# This is a reference for the prompt template for fixing the output format.
output_format_message='If it is mentioned, please answer {{oil field property/method name:mentioned/Reference page and content}}, \
Otherwise, please answer {{{eo_a}:not_mentioned}}.Please keep the curly braces in the answer and \
ensure answers are on separate rows. Do not add punctuation outside of curly braces or extra text.'

# pp_:prompt plaground
# _t:_test
# eo_: extraction object
def pp_ask_production_methods(eo_field:str):
    txt=f'write your prompt template about {eo_field} oil prodction methods.{output_format_message}'
    return txt

def pp_ask_field_properties(eo_field:str):
    txt=f'write your prompt template about {eo_field} oil filed properties.{output_format_message}'
    return txt

def pp_ask_fluid_properties(eo_field:str):
    txt=f'write your prompt template about {eo_field} oil fluid properties.{output_format_message}'
    return txt

def pp_ask_production_practies (eo_field:str):
    txt=f'write your prompt template about {eo_field} oil production practies.{output_format_message}'
    return txt

def pp_methods_and_properties():
    methods_and_properties= [pp_ask_production_methods,pp_ask_field_properties,pp_ask_fluid_properties,pp_ask_production_practies]
    return methods_and_properties
