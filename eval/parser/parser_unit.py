"""
Author: Alex <alex.hu@57blocks.com>
Date Created: 2023-10-19
Description: Unit parser class.
"""
import os
import sys
import re
from typing import Any
import pint

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../../')

from eval.parser.parser import Parser
from eval.parser.parser_utils import *
from eval.parser.parser_result import ParseResult, ParserSuccessResult, \
    ParserErrorResult
from lib.helper import split_at_first_char

pattern_number = r'([\d,]*(?:\.\d+\s*\d*)+|[\d,]+)\s*(\S*)'
pattern_split_unit_number = r'^([\d,]*\.\d+|[\d,]+)\s*(.*)'
MIN_T_OF_OIL = "min t of oil"
MIN_T_OF_OIL_UNIT = "min-t-of-oil"

DEG_API = 'deg.api'

DU_F = "° f"
DU_F_UNIT = "°-f"

DU_F_V2 = "degrees celsius"
DU_F_V2_UNIT = "degrees-celsius"

DU_F_V3 = "degrees fahrenheit"
DU_F_V3_UNIT = "degrees-fahrenheit"

DU_API = "º api"
DU_API_UNIT = "º-api"

DU_API_V2 = "°api"
DU_API_V2_UNIT = "deg.api"

WATER_OIL_RATIO = "water/oil ratio"
WATER_OIL_RATIO_UNIT = "water/oil-ratio"

BBL_INJ = "bbl inj/bbl oil"
BBL_INJ_UNIT = "bbl-inj/bbl-oil"

DU_API_V3 = "deg api"
DU_API_V3_UNIT = "deg-api"

DU_APU_V4 = "degrees api"
DU_APU_V4_UNIT = "degrees-api"

STB_PER_DAY = "stb per day"
STB_PER_DAY_UNIT = "stb-per-day"

STB_PER_DAY_V2 = "stock tank barrels (stb) per day"
STB_PER_DAY_V2_UNIT = "stock-tank-barrels-(stb)-per-day"
VOL_PER = 'vol %'
VOL_PER_UNIT = 'vol%'
MOLE_FRACTION = 'mole fraction'
MOLE_FRACTION_UNIT = 'mole-fraction'
pattern_range_number = r"(?:between|from|range)\s+(\d+\.?\d*)\s+(?:and|to)\s+(\d+\.?\d*)\s+([\w\-]+)"

pattern_number_range_with_to = r'(\d+[,.]?\d*)\s+(?:and|to)\s+(\d+[,.]?\d*)\s+([\w-]+)'

INJECTOR_TUBING_DIAMETER = 'Injector tubing diameter'
PRODUCER_TUBING_DIAMETER = 'Production tubing diameter'


class ParserUnit(Parser):
    '''
    Fields parser with units
    '''

    @handle_parser_error
    def parse(self,
              llm_raw_response: Any,
              key=None,
              unit=None) -> ParseResult:
        # CONCEPT: we call what LLM returns is raw
        # Then, the Parser try to parse and convert it to target units
        # llm_raw_response: original(value unit)@reference
        # parsed: parsed(target-value target-unit)@reference
        # TODO: refactor var names
        parse_content = split_at_first_char(llm_raw_response, SPLIT_REF_CHAR)
        parse_content = super().remove_qutoes(parse_content)
        parse_content = super().remove_commas(parse_content)
        raw_content = parse_content[0]
        parse_content[0] = parse_content[0].lower()

        cls_name = (type(self).__name__)

        if is_not_mentioned(parse_content[0]):
            parse_content[0] = np.nan
            return ParserSuccessResult.handle_success_response(
                llm_raw_response,
                parse_content,
                class_name=cls_name)
        raw_unit = unit.lower() if unit else unit

        if key == INJECTOR_TUBING_DIAMETER:
            err, parse_content[0] = extract_mixed_numbers(parse_content[0])
            if not err:
                return ParserSuccessResult.handle_success_response(
                    llm_raw_response,
                    parse_content,
                    unit=unit,
                    class_name=cls_name)
            else:
                parse_content[0] = raw_content.lower()

        parse_content[0] = parse_content[0].replace(MIN_T_OF_OIL,
                                                    MIN_T_OF_OIL_UNIT)
        parse_content[0] = parse_content[0].replace(STB_PER_DAY,
                                                    STB_PER_DAY_UNIT)
        parse_content[0] = parse_content[0].replace(DU_F, DU_F_UNIT)
        parse_content[0] = parse_content[0].replace(DU_API, DU_API_UNIT)
        parse_content[0] = parse_content[0].replace(DU_F_V2, DU_F_V2_UNIT)
        parse_content[0] = parse_content[0].replace(DU_API_V2, DU_API_V2_UNIT)
        parse_content[0] = parse_content[0].replace(DU_API_V3, DU_API_V3_UNIT)
        parse_content[0] = parse_content[0].replace(DU_APU_V4, DU_APU_V4_UNIT)
        parse_content[0] = parse_content[0].replace(WATER_OIL_RATIO,
                                                    WATER_OIL_RATIO_UNIT)
        parse_content[0] = parse_content[0].replace(BBL_INJ, BBL_INJ_UNIT)
        parse_content[0] = parse_content[0].replace(STB_PER_DAY_V2,
                                                    STB_PER_DAY_V2_UNIT)
        parse_content[0] = parse_content[0].replace(DU_F_V3, DU_F_V3_UNIT)
        parse_content[0] = parse_content[0].replace(VOL_PER, VOL_PER_UNIT)
        parse_content[0] = parse_content[0].replace(MOLE_FRACTION,
                                                    MOLE_FRACTION_UNIT)

        match = re.search(pattern_range_number, parse_content[0])
        if match:
            parse_content[
                0] = f"{match.group(1)}-{match.group(2)} {match.group(3)}"

        match = re.search(pattern_number_range_with_to, parse_content[0])
        if match:
            parse_content[
                0] = f"{match.group(1)}-{match.group(2)} {match.group(3)}"

        # em dash '—' support
        if "-" in parse_content[0] or "–" in parse_content[0]:
            parse_content[0] = get_average(parse_content[0], raw_unit)
        match = re.search(pattern_number, parse_content[0])
        if not match:
            parse_content[0] = raw_content
            return ParserErrorResult.handle_err_response(llm_raw_response,
                                                         parse_content,
                                                         class_name=cls_name)

        if key == INJECTOR_TUBING_DIAMETER:
            # parse the Injector tubing diameter value "¼-in".
            rst = parse_unicode_injector_tubing_diameter(parse_content)
            if rst:
                parse_content = rst
                match = re.search(pattern_number, str(parse_content[0]))
        if key == PRODUCER_TUBING_DIAMETER:
            # split content into value and unit
            temp_parse = parse_content[0].split()
            # convert the fraction to float
            parse_content[0] = unicode_fraction_to_float(temp_parse[0])
            # value includes unit
            if len(temp_parse) > 1:
                parse_content[0] = f'{parse_content[0]} {temp_parse[1]}'
            match = re.search(pattern_number, str(parse_content[0]))
        try:
            # split number & unit
            number, unit = match.groups()
            # Remove commas and spaces from the number
            number = number.replace(',', '').replace(' ', '')
            parse_content[0] = f'{number} {unit}'
            # no unit
            if not unit:
                # keep the parse value when key is PRODUCER_TUBING_DIAMETER
                if key != PRODUCER_TUBING_DIAMETER:
                    parse_content[0] = raw_content
                return ParserErrorResult.handle_err_response(llm_raw_response,
                                                             parse_content,
                                                             class_name=cls_name)
        except:
            parse_content[0] = raw_content
            return ParserErrorResult.handle_err_response(llm_raw_response,
                                                         parse_content,
                                                         class_name=cls_name)

        err = False
        try:
            # after preprocessing, we are ready to parse
            # CONCEPT: number unit
            # the assumption is the first word is the number
            # anything else is the unit
            string = parse_content[0].split()
            unit = ' '.join(string[1:])
            unit = unit.lower()

            if raw_unit != DEG_API and unit in unit_convert_map.keys():
                err, parse_content[0] = unit_convert(string[0], unit)
            else:
                logger.debug("Unit %s not a recognized unit.", unit)
                logger.debug('Use pint as last resort')
                # if pint cannot parse, it just returns string[0]
                parse_content[0] = PaserPint(string[0]).result

            # current unit
            unit = unit_convert_map.get(unit, unit)
            parse_content[0] = float(parse_content[0])
        except:
            parse_content[0] = raw_content
            return ParserErrorResult.handle_err_response(llm_raw_response,
                                                         parse_content,
                                                         class_name=cls_name)
        if err:
            parse_content[0] = raw_content
            return ParserErrorResult.handle_err_response(llm_raw_response,
                                                         parse_content,
                                                         class_name=cls_name)
        # ignore DEG API unit
        if raw_unit != DEG_API and raw_unit and raw_unit != unit:
            # keep the parse value when key is PRODUCER_TUBING_DIAMETER
            if key != PRODUCER_TUBING_DIAMETER:
                parse_content[0] = raw_content
            return ParserErrorResult.handle_err_response(llm_raw_response,
                                                         parse_content,
                                                         class_name=cls_name)

        return ParserSuccessResult.handle_success_response(llm_raw_response,
                                                           parse_content,
                                                           unit=unit,
                                                           class_name=cls_name)


class PaserPint():
    '''
    use pint to parse the input
    '''

    def __init__(self, raw_val_unit: str, target_unit: str = None):
        '''
        :param raw_val_unit: raw value and/or unit
        :param target_unit: we shall know what property we ask
                            and what unit we want
        '''
        self._ureg = pint.UnitRegistry()
        self.input = raw_val_unit
        # default result is the input itself
        self._result = raw_val_unit
        self.target_unit = target_unit
        self.parse()

    def parse(self):
        '''
        :use pint to parse the input
        '''
        try:
            quantity = self._ureg.parse_expression(self.input)
            if not isinstance(quantity, pint.Quantity):
                self._result = quantity
                return
        except pint.errors as e:
            logger.error('pint cannot parse either %s because of %s',
                         self.input,
                         e)
            return

        # TODO: need to pass target unit
        if self.target_unit == 'inch':
            if quantity.units.is_compatible_with(self._ureg.inch):
                inch = quantity.to(self._ureg.inch).magnitude
                self._result = inch
                return
            else:
                logger.error('pint cannot convert %s to inch', self.input)

        # pint does not define some units we eed
        # [psia, scf/bbl oil, barrel (not mass in pint), md,
        if quantity.units.is_compatible_with(self._ureg.feet):
            feet = quantity.to(self._ureg.feet).magnitude
            self._result = feet
        elif quantity.units.is_compatible_with(
                self._ureg.Unit('barrel / day')):
            bbld = quantity.to(self._ureg.Unit('barrel / day')).magnitude
            self._result = bbld
        else:
            logger.error('pint cannot find compatible units for %s',
                         self.input)
            # directly take the magnitude
            self._result = quantity.magnitude

    @property
    def result(self):
        ''' getter of result '''
        return self._result


def main():
    ''' in file test '''
    print(PaserPint('1.5 feet', 'inch').result)
    data = ParserUnit().parse("1 ¼-in.", unit='inch',
                              key=INJECTOR_TUBING_DIAMETER)
    print(data)


if __name__ == '__main__':
    main()
