from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Callable, List

from eval.parser.parser_category import ParserCategory
from eval.parser.parser_mention import ParserMentioned
from eval.parser.parser_text import ParserText
from eval.parser.parser_time import ParserTime
from eval.parser.parser_numeric import ParserNumeric
from eval.parser.parser_unit import ParserUnit
from eval.parser.parser import Parser
from eval.merger.merger import Merger

# production methods (9 vars)
VAR_SEC1_DOWNHOLE_PUMP = 'Downhole pump'
VAR_SEC1_WATER_REINJECTION = "Water reinjection"
VAR_SEC1_NATURAL_GAS_REINJECTION = 'Natural gas reinjection'
VAR_SEC1_WATER_FLOODING = "Water flooding"
VAR_SEC1_GAS_LIFTING = 'Gas lifting'
VAR_SEC1_GAS_FLOODING = 'Gas flooding'
VAR_SEC1_STEAM_FLOODING = 'Steam flooding'
VAR_SEC1_OIL_SANDS_MINE_I = 'Oil sands mine (integrated with upgrader)'
VAR_SEC1_OIL_SANDS_MINE_NI = 'Oil sands mine (non-integrated with upgrader)'
# Field properties (13 vars)
VAR_SEC2_FIELD_LOCATION = 'Field location (Country)'
VAR_SEC2_FIELD_NAME = 'Field name'
VAR_SEC2_FIELD_AGE = 'Field age'
VAR_SEC2_FIELD_DEPTH = 'Field depth'
VAR_SEC2_PRODUCTION_VOLUME = 'Oil production volume'
VAR_SEC2_NUM_OF_PRODUCING_WELLS = 'Number of producing wells'
VAR_SEC2_NUM_OF_WATER_INJECTING_WELLS = 'Number of water injecting wells'
VAR_SEC2_PRODUCTION_TUBING_DIAMETER = 'Production tubing diameter'
VAR_SEC2_INJECTOR_TUBING_DIAMETER = 'Injector tubing diameter'
VAR_SEC2_BOTTOMHOLE_PRESSURE = 'Bottomhole pressure'
VAR_SEC2_RESERVOIR_PRESSURE = 'Reservoir pressure'
VAR_SEC2_RESERVOIR_TEMPERATURE = 'Reservoir temperature'
VAR_SEC2_OFFSHORE = 'Offshore'
# Fluid properties (8 vars)
VAR_SEC3_API_GRAVITY = 'API gravity (oil at standard pressure and temperature, or "dead oil")'
VAR_SEC3_N2 = 'N2'
VAR_SEC3_CO2 = 'CO2'
VAR_SEC3_C1 = 'C1'
VAR_SEC3_C2 = 'C2'
VAR_SEC3_C3 = 'C3'
VAR_SEC3_C4_PLUS = 'C4+'
VAR_SEC3_H2S = 'H2S'
# Production practices (15 vars)
VAR_SEC4_GOR = 'Gas-to-oil ratio (GOR)'
VAR_SEC4_WOR = 'Water-to-oil ratio (WOR)'
VAR_SEC4_WATER_INJECTION_RATIO = 'Water injection ratio'
VAR_SEC4_GAS_LIFTING_INJECTION_RATIO = 'Gas lifting injection ratio'
VAR_SEC4_GAS_FLOODING_INJECTION_RATIO = 'Gas flooding injection ratio'
VAR_SEC4_FLOOD_GAS = 'Flood gas'
VAR_SEC4_F_OF_CO2 = 'Fraction of CO2 breaking through to producers'
VAR_SEC4_SOURCE_OF_MAKEUP_CO2 = 'Source of makeup CO2'
VAR_SEC4_P_OF_SEQUESTRATION = 'Percentage of sequestration credit assigned to the oilfield'
VAR_SEC4_SOR = 'Steam-to-oil ratio (SOR)'
VAR_SEC4_F_OF_FOSSIL = 'Fraction of required fossil electricity generated onsite'
VAR_SEC4_F_OF_NGAS = 'Fraction of remaining natural gas reinjected'
VAR_SEC4_F_OF_WATER_REINJECTED = 'Fraction of produced water reinjected'
VAR_SEC4_F_OF_STEAM_COG = 'Fraction of steam generation via cogeneration'
VAR_SEC4_F_OF_STEAM_SOLAR = 'Fraction of steam generation via solar thermal'
# Processing practices (6 vars)
VAR_SEC5_HEATER_TREATER = 'Heater/treater'
VAR_SEC5_STABILIZER_COLUMN = 'Stabilizer column'
VAR_SEC5_UPGRADER_TYPE = 'Upgrader type'
VAR_SEC5_FLARING_TO_OIL_RATIO = 'Flaring-to-oil ratio'
VAR_SEC5_VENTING_FRACTION = 'Venting fraction (purposeful venting of post-flare gas)'
VAR_SEC5_VOLUME_FRACTION_OF_DILUENT = 'Volume fraction of diluent'
# Others (5 vars)
VAR_SEC6_EXCESS_PRESSURE = \
'Excess pressure in injector well (injector well interface flowing pressure - avg res. pressure)'
VAR_SEC6_RESERVOIR_PERMEABILITY = 'Reservoir permeability'
VAR_SEC6_RESERVOIR_THICKNESS = 'Reservoir thickness'
VAR_SEC6_WELLHEAD_PRESSURE = 'Wellhead pressure'
VAR_SEC6_WELLHEAD_TEMPERATURE = 'Wellhead temperature'

# Section 9: helpers that used to caculate other attribute
# we just name it as section 9
VAR_SEC9_OIL_PRODUCTION_BOPD = 'Oil_Production_BOPD'
VAR_SEC9_Gas_Production_Mmscfd = 'Gas_Production_Mmscfd'

helper_variables = [VAR_SEC9_OIL_PRODUCTION_BOPD, VAR_SEC9_Gas_Production_Mmscfd]

@dataclass
class Variable:
    value_parser: Optional[Parser | Callable]
    merger: Optional[Merger | Callable]
    name_parser: ParserText = ParserText
    ref_merger: Merger = Merger
    raw_text_merger: Merger = Merger
    status_merger: Merger = Merger

    name: str = ''
    section: str = ''
    unit: str = ''
    prompt: str = ''
    gt_row: int = 0           # Row index in Ground Truth

    # True if variable is in ground truth and need to be evaluated,
    # False is middle variable used to calculate other variable.
    is_in_gt: bool = True

    def __str__(self):
        return f"name: {self.name}, section: {self.section}, unit: {self.unit}"


variable_list = [
        # Production methods
        Variable(name="Downhole pump", section='Production methods', value_parser=ParserMentioned,
                 merger=Merger, gt_row=9),
        Variable(name="Water reinjection", section='Production methods', value_parser=ParserMentioned,
                 merger=Merger, gt_row=10),
        Variable(name="Natural gas reinjection", section='Production methods', value_parser=ParserMentioned,
                 merger=Merger, gt_row=11),
        Variable(name="Water flooding", section='Production methods', value_parser=ParserMentioned,
                 merger=Merger, gt_row=12),
        Variable(name="Gas lifting", section='Production methods', value_parser=ParserMentioned,
                 merger=Merger, gt_row=13),
        Variable(name="Gas flooding", section='Production methods', value_parser=ParserMentioned,
                 merger=Merger, gt_row=14),
        Variable(name="Steam flooding", section='Production methods', value_parser=ParserMentioned,
                 merger=Merger, gt_row=15),
        Variable(name="Oil sands mine (integrated with upgrader)", section='Production methods',
                 value_parser=ParserMentioned, merger=Merger, gt_row=16),
        Variable(name="Oil sands mine (non-integrated with upgrader)", section='Production methods',
                 value_parser=ParserMentioned, merger=Merger, gt_row=17),

        # Field properties
        Variable(name="Field location (Country)", section='Field properties', value_parser=ParserText,
                 merger=Merger, gt_row=20),
        Variable(name="Field name", section='Field properties', value_parser=ParserText, merger=Merger,
                 gt_row=21),
        Variable(name="Field age", section='Field properties', unit='yr', value_parser=ParserTime,
                 merger=Merger, gt_row=22),
        Variable(name="Field depth", section='Field properties', unit='ft', value_parser=ParserUnit,
                 merger=Merger, gt_row=23),
        Variable(name="Oil production volume", section='Field properties', unit='bbl/d', value_parser=ParserUnit,
                 merger=Merger, gt_row=24),
        Variable(name="Number of producing wells", section='Field properties', value_parser=ParserNumeric,
                 merger=Merger, gt_row=25),
        Variable(name="Number of water injecting wells", section='Field properties', value_parser=ParserNumeric,
                 merger=Merger, gt_row=26),
        Variable(name="Production tubing diameter", section='Field properties', unit='in', value_parser=ParserUnit,
                 merger=Merger, gt_row=27),
        Variable(name="Injector tubing diameter", section='Field properties', unit='in', value_parser=ParserUnit,
                 merger=Merger, gt_row=28),
        Variable(name="Bottomhole pressure", section='Field properties', unit='psia', value_parser=ParserUnit,
                 merger=Merger, gt_row=29),
        Variable(name="Reservoir pressure", section='Field properties', unit='psia', value_parser=ParserUnit,
                 merger=Merger, gt_row=30),
        Variable(name="Reservoir temperature", section='Field properties', unit='°f', value_parser=ParserUnit,
                 merger=Merger, gt_row=31),
        Variable(name="Offshore", section='Field properties', value_parser=ParserNumeric, merger=Merger, gt_row=32),

        # Fluid properties
        Variable(name='API gravity (oil at standard pressure and temperature, or "dead oil")',
                 section='Fluid properties', unit='deg.API', value_parser=ParserUnit, merger=Merger, gt_row=34),
        Variable(name='N2', section='Fluid properties', unit='mol%', value_parser=ParserUnit, merger=Merger,
                 gt_row=36),
        Variable(name='CO2', section='Fluid properties', unit='mol%', value_parser=ParserUnit, merger=Merger,
                 gt_row=37),
        Variable(name='C1', section='Fluid properties', unit='mol%', value_parser=ParserUnit, merger=Merger,
                 gt_row=38),
        Variable(name='C2', section='Fluid properties', unit='mol%', value_parser=ParserUnit, merger=Merger,
                 gt_row=39),
        Variable(name='C3', section='Fluid properties', unit='mol%', value_parser=ParserUnit, merger=Merger,
                 gt_row=40),
        Variable(name='C4+', section='Fluid properties', unit='mol%', value_parser=ParserUnit, merger=Merger,
                 gt_row=41),
        Variable(name='H2S', section='Fluid properties', unit='mol%', value_parser=ParserUnit, merger=Merger,
                 gt_row=42),

        # Production practices
        Variable(name='Gas-to-oil ratio (GOR)', section='Production practices', unit='scf/bbl oil',
                 value_parser=ParserUnit, merger=Merger, gt_row=46),
        Variable(name='Water-to-oil ratio (WOR)', section='Production practices', unit='bbl water/bbl oil',
                 value_parser=ParserUnit, merger=Merger, gt_row=47),
        Variable(name='Water injection ratio', section='Production practices', unit='bbl water/bbl oil',
                 value_parser=ParserUnit, merger=Merger, gt_row=48),
        Variable(name='Gas lifting injection ratio', section='Production practices', unit='scf/bbl liquid',
                 value_parser=ParserUnit, merger=Merger, gt_row=49),
        Variable(name='Gas flooding injection ratio', section='Production practices', unit='scf/bbl oil',
                 value_parser=ParserUnit, merger=Merger, gt_row=50),
        Variable(name='Flood gas', section='Production practices', value_parser=ParserCategory, merger=Merger,
                 gt_row=51),
        Variable(name='Fraction of CO2 breaking through to producers', section='Production practices', unit='%',
                 value_parser=ParserUnit, merger=Merger, gt_row=58),
        Variable(name='Source of makeup CO2', section='Production practices', value_parser=ParserCategory,
                 merger=Merger, gt_row=59),
        Variable(name='Percentage of sequestration credit assigned to the oilfield', section='Production practices',
                 unit='%', value_parser=ParserUnit, merger=Merger, gt_row=62),
        Variable(name='Steam-to-oil ratio (SOR)', section='Production practices', unit='bbl steam/bbl oil',
                 value_parser=ParserUnit, merger=Merger, gt_row=63),
        Variable(name='Fraction of required fossil electricity generated onsite', section='Production practices',
                 value_parser=ParserNumeric, merger=Merger, gt_row=64),
        Variable(name='Fraction of remaining natural gas reinjected', section='Production practices',
                 value_parser=ParserNumeric, merger=Merger, gt_row=65),
        Variable(name='Fraction of produced water reinjected', section='Production practices',
                 value_parser=ParserNumeric, merger=Merger, gt_row=66),
        Variable(name='Fraction of steam generation via cogeneration', section='Production practices',
                 value_parser=ParserNumeric, merger=Merger, gt_row=67),
        Variable(name='Fraction of steam generation via solar thermal', section='Production practices',
                 value_parser=ParserNumeric, merger=Merger, gt_row=68),

        # Middle variables used to calculate other variable
        Variable(name='Oil_Production_BOPD', section='Production practices',
                 value_parser=ParserNumeric, merger=Merger, is_in_gt=False),
        Variable(name='Gas_Production_Mmscfd', section='Production practices',
                         value_parser=ParserNumeric, merger=Merger, is_in_gt=False),

        # Processing practices
        Variable(name="Heater/treater", section='Processing practices', value_parser=ParserMentioned,
                 merger=Merger, gt_row=70),
        Variable(name="Stabilizer column", section='Processing practices', value_parser=ParserMentioned,
                 merger=Merger, gt_row=71),
        Variable(name="Upgrader type", section='Processing practices', value_parser=ParserCategory, merger=Merger,
                 gt_row=72),
        Variable(name="Flaring-to-oil ratio", section='Processing practices', unit='scf/bbl oil',
                 value_parser=ParserUnit, merger=Merger, gt_row=77),
        Variable(name="Venting fraction (purposeful venting of post-flare gas)", section='Processing practices',
                 unit='fraction post-flare gas', value_parser=ParserUnit, merger=Merger, gt_row=78),
        Variable(name="Volume fraction of diluent", section='Processing practices', value_parser=ParserNumeric,
                 merger=Merger, gt_row=80),

        # Others
        Variable(name='Excess pressure in injector well (injector well interface flowing pressure - avg res. pressure)',
                 section='Others', unit='psia', value_parser=ParserUnit, merger=Merger, gt_row=81),
        Variable(name='Reservoir permeability', section='Others', unit='mD', value_parser=ParserUnit,
                 merger=Merger, gt_row=82),
        Variable(name='Reservoir thickness', section='Others', unit='ft', value_parser=ParserUnit,
                 merger=Merger, gt_row=83),
        Variable(name='Wellhead pressure', section='Others', unit='psia', value_parser=ParserUnit,
                 merger=Merger, gt_row=84),
        Variable(name='Wellhead temperature', section='Others', unit='°f', value_parser=ParserUnit,
                 merger=Merger, gt_row=85),
]


def get_units(variables: List[str]) -> List[str]:
    units = []
    for var in variables:
        for var_obj in variable_list:
            if var.lower() == var_obj.name.lower():
                units.append(var_obj.unit)

    return units


def get_units_all() -> List[str]:
    units = []
    for var_obj in variable_list:
        if var_obj.is_in_gt:
            units.append(var_obj.unit)

    return units


def get_variable(section: str = None, var_names: List[str] = None, ignore: List[str] = [], only_gt=True) -> List[Variable]:
    if section:
        return _get_var_by_section(section, ignore=ignore, only_gt=only_gt)
    if var_names:
        return _get_var_by_name([name.lower() for name in var_names])
    if section and var_names:
        return (_get_var_by_section(section, ignore=ignore, only_gt=only_gt)
                + _get_var_by_name([name.lower() for name in var_names])
                )

    return []


# Return variable names added in v2 ground truth update.
def get_v2_variables() -> List[str]:
    v2_variables = [var.name for var in _get_var_by_section('Others')]
    v2_variables .append('Bottomhole pressure')
    return v2_variables


def _get_var_by_section(section: str, ignore: List[str] = [], only_gt: bool = True) -> List[Variable]:
    var_list = []
    for var in variable_list:
        if var.section.lower() == section.lower() and var.name not in ignore:
            if only_gt:
                if var.is_in_gt:
                    var_list.append(var)
            else:
                var_list.append(var)

    return var_list


def _get_var_by_name(var_names: List[str]) -> List[Variable]:
    var_list = []
    for var in variable_list:
        if var.name.lower() in var_names:
            var_list.append(var)

    return var_list


def get_all_variable(only_gt: bool = False) -> List[Variable]:
    var_list = []
    for var in variable_list:
        if only_gt:
            if var.is_in_gt:
                var_list.append(var)
        else:
            var_list.append(var)
    return var_list


def is_gt_variable(var_name: str):
    var_obj = get_variable(var_names=[var_name])[0]
    return var_obj.is_in_gt


