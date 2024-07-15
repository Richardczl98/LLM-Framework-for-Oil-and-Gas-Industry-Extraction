from unittest import TestCase
from pathlib import Path
import numpy as np
import datetime

from config import ROOT_DIR, YEAR_FOR_CALUCULATION
from eval.parser.client import ParserClient
from eval.parser.parser_result import ParserErrorResult, ParserData

data_file_path = Path(ROOT_DIR, 'tests/testdata/eval/parser/data_parser.yaml')


def assert_succeed_responses(want, succeed_resp):
    for resp in succeed_resp:
        print(resp.variable.name)
        if isinstance(want[resp.variable.name]['value'], float) and np.isnan(want[resp.variable.name]['value']):
            assert np.isnan(resp.result.data.value)
        else:
            assert resp.result.data.value == want[resp.variable.name]['value']
        assert resp.result.data.unit == want[resp.variable.name]['unit']
        assert resp.result.data.ref == want[resp.variable.name]['ref']


def assert_failed_responseonses(error, failed_response):
    for err_resp, get_resp in zip(error['failed_responseonses'], failed_response):
        assert err_resp['field'] == get_resp.field
        assert err_resp['section'] == get_resp.section
        assert err_resp['record'] == get_resp.record
        assert err_resp['variable'] == get_resp.variable
        assert err_resp['result'].status == get_resp.result.status


def show_resp(responses, show_type=False):
    for resp in responses:
        if resp.result.status == 'success':
            print(f"'{resp.variable.name}': " + '{' + f"'value': {resp.result.data.value}, 'unit': {resp.result.data.unit}, 'ref': {resp.result.data.ref}" + '},')
            if show_type:
                print(f"'{resp.variable.name}': " + '{' + f"'value': {type(resp.result.data.value)}, 'unit': {type(resp.result.data.unit)}, 'ref': {type(resp.result.data.ref)}" + '},')
        else:
            print('------------ failed ------------')
            print(f"'field': {resp.field},\n 'section': {resp.section},\n 'record': {resp.record},\n 'variable': {resp.variable}, \n 'result': {resp.result}, ")
            if show_type:
                print(f"'field': {type(resp.field)},\n 'section': {type(resp.section)},\n 'record': {type(resp.record)},\n 'variable': {type(resp.variable)}, \n 'result': {type(resp.result)}, ")


class TestParserProductionMethods(TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_parse_mentioned(self):
        client = ParserClient(model='test_model', field_name='test_field', section='Production methods')
        data = '{Downhole pump:not_mentioned}\n{Water reinjection:not_mentioned}\n{Natural gas reinjection:not_mentioned}\n{Water flooding:not_mentioned}\n{Gas lifting:not_mentioned}\n{Gas flooding:not_mentioned}\n{Steam flooding:mentioned@Page 6/ "Okha5,18 (Sakhalin) ",1965-2006 ,500-700 ,Clastic 0.1-1.2 ,80-600 ,"Huff and puff in individual blocks of field started in 1962. Steam flooding in individual blocks was carried out from 1973 to 1987. Total injection: steam: 16.5 MMtons, water: 65.5 MMtons. Additional oil production: 5.6 MMtons (35.7 % total oil production). Steam oil ratio (SOR):  3.0"}\n{Oil sands mine (integrated with upgrader):not_mentioned}\n{Oil sands mine (non-integrated with upgrader):not_mentioned}'
        want = {
            'Downhole pump': {'value': np.nan, 'unit': '', "ref": ''},
            'Water reinjection': {'value': np.nan, 'unit': '', "ref": ''},
            'Natural gas reinjection': {'value': np.nan, 'unit': '', "ref": ''},
            'Water flooding': {'value': np.nan, 'unit': '', "ref": ''},
            'Gas lifting': {'value': np.nan, 'unit': '', "ref": ''},
            'Gas flooding': {'value': np.nan, 'unit': '', "ref": ''},
            'Steam flooding': {'value': 1.0, 'unit': '', 'ref': 'Page 6/ "Okha5,18 (Sakhalin) ",1965-2006 ,500-700 ,Clastic 0.1-1.2 ,80-600 ,"Huff and puff in individual blocks of field started in 1962. Steam flooding in individual blocks was carried out from 1973 to 1987. Total injection: steam: 16.5 MMtons, water: 65.5 MMtons. Additional oil production: 5.6 MMtons (35.7 % total oil production). Steam oil ratio (SOR):  3.0"'},
            'Oil sands mine (integrated with upgrader)': {'value': np.nan, 'unit': '', "ref": ''},
            'Oil sands mine (non-integrated with upgrader)': {'value': np.nan, 'unit': '', "ref": ''},
        }
        client.parse_llm_response(data)
        assert_succeed_responses(want, client.responses)

    def test_parse_miss_key_value(self):
        client = ParserClient(model='test_model', field_name='test_field', section='Field properties')
        data = '{Field location (Country): Sakhalin, Russia@Reference page 6}\n{Field age:not_mentioned}\n{Field depth:not_mentioned}\n{Oil production volume:not_mentioned}\n{Number of producing wells:not_mentioned}\n{Number of water injecting wells:not_mentioned}\n{Production tubing diameter:not_mentioned}\n{Productivity index:not_mentioned}\n{Reservoir pressure:not_mentioned}\n{Reservoir temperature:not_mentioned}'
        want = {
            'Field location (Country)': {'value': 'Sakhalin, Russia', 'unit': '', 'ref': 'Reference page 6'},
            'Field name': {'value': 'Russia', 'unit': '', 'ref': ''},
            'Field age': {'value': np.nan, 'unit': '', 'ref': ''},
            'Field depth': {'value': np.nan, 'unit': '', 'ref': ''},
            'Oil production volume': {'value': np.nan, 'unit': '', 'ref': ''},
            'Number of producing wells': {'value': np.nan, 'unit': '', 'ref': ''},
            'Number of water injecting wells': {'value': np.nan, 'unit': '', 'ref': ''},
            'Production tubing diameter': {'value': np.nan, 'unit': '', 'ref': ''},
            'Productivity index': {'value': np.nan, 'unit': '', 'ref': ''},
            'Reservoir pressure': {'value': np.nan, 'unit': '', 'ref': ''},
            'Reservoir temperature': {'value': np.nan, 'unit': '', 'ref': ''},
            # 'Offshore': {'value': np.nan, 'unit': '', 'ref': ''},
        }
        error = {
            'failed_responseonses': [
                {
                    'field': 'test_field',
                    'section': 'Field properties',
                    'record': '{Field location (Country): Sakhalin, Russia@Reference page 6}\n{Field age:not_mentioned}\n{Field depth:not_mentioned}\n{Oil production volume:not_mentioned}\n{Number of producing wells:not_mentioned}\n{Number of water injecting wells:not_mentioned}\n{Production tubing diameter:not_mentioned}\n{Productivity index:not_mentioned}\n{Reservoir pressure:not_mentioned}\n{Reservoir temperature:not_mentioned}',
                    'variable': None,
                    'result': ParserErrorResult(data=ParserData(), status='error'),
                },
            ]
        }
        client.parse_llm_response(data)
        # show_resp(client.failed_response)

        assert_succeed_responses(want, client.responses)
        assert_failed_responseonses(error, client.failed_response)

    def test_parse_colon_error(self):
        client = ParserClient(model='test_model', field_name='test_field', section='Field properties')
        data = '{Field location (Country): Sakhalin, Russia@Reference page 6}\n{Field age;not_mentioned}\n{Field depth:not_mentioned}\n{Oil production volume:not_mentioned}\n{Number of producing wells:not_mentioned}\n{Number of water injecting wells:not_mentioned}\n{Production tubing diameter:not_mentioned}\n{Productivity index:not_mentioned}\n{Reservoir pressure:not_mentioned}\n{Reservoir temperature:not_mentioned}\n{Offshore:not_mentioned}'
        want = {
            'Field location (Country)': {'value': 'Sakhalin, Russia', 'unit': '', 'ref': 'Reference page 6'},
            'Field age': {'value': np.nan, 'unit': '', 'ref': ''},
            'Field depth': {'value': np.nan, 'unit': '', 'ref': ''},
            'Oil production volume': {'value': np.nan, 'unit': '', 'ref': ''},
            'Number of producing wells': {'value': np.nan, 'unit': '', 'ref': ''},
            'Number of water injecting wells': {'value': np.nan, 'unit': '', 'ref': ''},
            'Production tubing diameter': {'value': np.nan, 'unit': '', 'ref': ''},
            'Productivity index': {'value': np.nan, 'unit': '', 'ref': ''},
            'Reservoir pressure': {'value': np.nan, 'unit': '', 'ref': ''},
            'Reservoir temperature': {'value': np.nan, 'unit': '', 'ref': ''},
            'Offshore': {'value': np.nan, 'unit': '', 'ref': ''},
        }
        error = {
            'failed_responseonses': [
                {
                    'field': 'test_field',
                    'section': 'Field properties',
                    'record': 'Field age;not_mentioned',
                    'variable': None,
                    'result': ParserErrorResult(data=ParserData(), status='error'),
                },
            ]
        }
        client.parse_llm_response(data)
        # show_resp(client.failed_response)

        assert_succeed_responses(want, client.responses)
        assert_failed_responseonses(error, client.failed_response)

    def test_parse_numeric(self):
        client = ParserClient(model='test_model', field_name='test_field', section='Field properties')
        data = '{Field location (Country): Brazil}\n{Field age: not_mentioned}\n{Field depth: "2,297" ft, Information from page 4 "Depth (ft) ,-,"2,297""}\n{Oil production volume: not_mentioned}\n{Number of producing wells: not_mentioned}\n{Number of water injecting wells: not_mentioned}\n{Production tubing diameter: not_mentioned}\n{Productivity index: not_mentioned}\n{Reservoir pressure: not_mentioned}\n{Reservoir temperature: 122 °F, Information from page 4 "Temperature (⁰F) ,< 176 ,122"}\n{Offshore: not_mentioned}'
        want = {
            'Field location (Country)': {'value': 'Brazil', 'unit': '', 'ref': ''},
            'Field age': {'value': np.nan, 'unit': '', 'ref': ''},
            'Field depth': {'value': 2297.0, 'unit': 'ft', 'ref': ''},
            'Oil production volume': {'value': np.nan, 'unit': '', 'ref': ''},
            'Number of producing wells': {'value': np.nan, 'unit': '', 'ref': ''},
            'Number of water injecting wells': {'value': np.nan, 'unit': '', 'ref': ''},
            'Production tubing diameter': {'value': np.nan, 'unit': '', 'ref': ''},
            'Productivity index': {'value': np.nan, 'unit': '', 'ref': ''},
            'Reservoir pressure': {'value': np.nan, 'unit': '', 'ref': ''},
            'Reservoir temperature': {'value': 122.0, 'unit': '°f', 'ref': ''},
            'Offshore': {'value': np.nan, 'unit': '', 'ref': ''},
        }
        client.parse_llm_response(data)
        # show_resp(client.responses)
        assert_succeed_responses(want, client.responses)

    def test_parse_time_pressure(self):
        client = ParserClient(model='test_model', field_name='test_field', section='Field properties')
        data = '{Field location (Country): Venezuela@Reference page and content: page 1 ""The Lagunillas 07 reservoir is located Lake Maracaibo in Venezuela.""}\n{Field age: Started production in 1926, Reference page and content: page 1 ""Oil production began in 1926.""}\n{Field depth: not_mentioned}\n{Oil production volume: More than 1,000 wells have been drilled since 1926 and 36.7 % of the initial oil in place had been produced by December 1999, Reference page and content: page 1 ""Oil production began in 1926 and more than 1,000 wells have been drilled. By December 1999...36.7 % of the initial oil in place had been produced.""}\n{Number of producing wells: More than 1,000, Reference page and content: page 1 ""Oil production began in 1926 and more than 1,000 wells have been drilled.""}\n{Number of water injecting wells: 15 initially, but only 12 were active, Reference page and content: page 2 ""Fifteen injector wells were drilled in the southern part of the reservoir in 1984. But, only 12 of the wells were active.""}\n{Production tubing diameter: not_mentioned}\n{Productivity index: not_mentioned}\n{Reservoir pressure: Initial pressure was 1785 psia at a datum of 3,700 feet subsea and it declined to 788 psia in 1980 before increasing to 950 psia in 1999 due to water injection, Reference page and content: page 2 ""Figures 3 shows...the average reservoir pressure at a datum of 3,700 ft.ss. declined exponentially...The average reservoir pressure increased from 753 psia in 1984 to 950 psia in 1999 in response to the water injection.""}\n{Reservoir temperature: 152 oF, Reference page and content: page 1 ""The reservoir temperature was 152 oF.""}\n{Offshore: not_mentioned}'
        want = {
            'Field location (Country)': {'value': 'Venezuela', 'unit': '', 'ref': 'Reference page and content: page 1 ""The Lagunillas 07 reservoir is located Lake Maracaibo in Venezuela.""'},
            'Field age': {'value': YEAR_FOR_CALUCULATION - 1926, 'unit': '', 'ref': ''},
            'Field depth': {'value': np.nan, 'unit': '', 'ref': ''},
            'Oil production volume': {'value': 1000, 'unit': 'wells', 'ref': ''},
            'Number of producing wells': {'value': 1000, 'unit': '', 'ref': ''},
            'Number of water injecting wells': {'value': 15, 'unit': '', 'ref': ''},
            'Production tubing diameter': {'value': np.nan, 'unit': '', 'ref': ''},
            'Productivity index': {'value': np.nan, 'unit': '', 'ref': ''},
            'Reservoir pressure': {'value': 1785, 'unit': 'psia', 'ref': ''},
            'Reservoir temperature': {'value': 152.0, 'unit': '°f', 'ref': ''},
            'Offshore': {'value': np.nan, 'unit': '', 'ref': ''},
        }
        client.parse_llm_response(data)
        show_resp(client.responses, show_type=True)
        show_resp(client.failed_response)
        assert_succeed_responses(want, client.responses)

    def test_parse_range_value(self):
        client = ParserClient(model='test_model', field_name='test_field', section='Field properties')
        data = "{Field location (Country): South Oman@Reference page 1, ""The field under discussion is located on the Eastern flank of South Oman salt basin""}\n{Field age:not_mentioned}\n{Field depth: 550-675 m sub-sea (ss)/Reference page 1, ""at depth ranges of 550-675 m sub-sea (ss)""}\n{Oil production volume:not_mentioned}\n{Number of producing wells: 60/Reference page 1, ""The reservoir has been on production since 1980 and currently has about 70 active wells of which 60 are oil producers""}\n{Number of water injecting wells: 10/Reference page 1, ""The reservoir has been on production since 1980 and currently has about 70 active wells of which 60 are oil producers and 10 are water injectors""}\n{Production tubing diameter:not_mentioned}\n{Productivity index:not_mentioned}\n{Reservoir pressure:not_mentioned}\n{Reservoir temperature:not_mentioned}\n{Offshore:not_mentioned}"
        want = {
            'Field location (Country)': {'value': 'South Oman', 'unit': '', 'ref': 'Reference page 1, The field under discussion is located on the Eastern flank of South Oman salt basin'},
            'Field age': {'value': np.nan, 'unit': '', 'ref': ''},
            'Field depth': {'value': 2009.0, 'unit': 'ft', 'ref': ''},
            'Oil production volume': {'value': np.nan, 'unit': '', 'ref': ''},
            'Number of producing wells': {'value': 60.0, 'unit': '', 'ref': ''},
            'Number of water injecting wells': {'value': 10.0, 'unit': '', 'ref': ''},
            'Production tubing diameter': {'value': np.nan, 'unit': '', 'ref': ''},
            'Productivity index': {'value': np.nan, 'unit': '', 'ref': ''},
            'Reservoir pressure': {'value': np.nan, 'unit': '', 'ref': ''},
            'Reservoir temperature': {'value': np.nan, 'unit': '', 'ref': ''},
            'Offshore': {'value': np.nan, 'unit': '', 'ref': ''},
        }
        client.parse_llm_response(data)
        # show_resp(client.responses)
        # show_resp(client.failed_response)
        assert_succeed_responses(want, client.responses)

    def test_parse_exception_record(self):
        client = ParserClient(model='test_model', field_name='test_field', variables=['Field location (Country)'])
        data = "{South Oman: not_mentioned}"
        # want = {
        #     'Field location (Country)': {'value': 'South Oman', 'unit': '', 'ref': 'Reference page 1, The field under discussion is located on the Eastern flank of South Oman salt basin'},
        # }
        client.parse_llm_response(data)
        # show_resp(client.responses)
        show_resp(client.failed_responses + client.unparsed_responses)
        # assert_succeed_responses(want, client.responses)

    def test_parse_exception_record_1(self):
        client = ParserClient(model='test_model', field_name='test_field', variables=['Field age'])
        data = "Field age:24@page 9"
        # want = {
        #     'Field location (Country)': {'value': 'South Oman', 'unit': '', 'ref': 'Reference page 1, The field under discussion is located on the Eastern flank of South Oman salt basin'},
        # }
        client.parse_llm_response(data)
        # show_resp(client.responses)
        show_resp(client.failed_responses + client.unparsed_responses)
        # assert_succeed_responses(want, client.responses)

    def test_parse_fluid_properties(self):
        client = ParserClient(model='test_model', field_name='test_field', section='Fluid properties')
        data = '{API gravity (oil at standard pressure and temperature, or "dead oil"):34@Reference page 4, Table 1}\n{N2:not_mentioned}\n{CO2:not_mentioned}\n{C1:not_mentioned}\n{C2:not_mentioned}\n{C3:not_mentioned}\n{C4+:not_mentioned}\n{H2S:not_mentioned}'
        want = {
            'API gravity (oil at standard pressure and temperature, or "dead oil")': {'value': 34, 'unit': '', 'ref': 'Reference page 4, Table 1'},
            'N2': {'value': np.nan, 'unit': '', 'ref': ''},
            'CO2': {'value': np.nan, 'unit': '', 'ref': ''},
            'C1': {'value': np.nan, 'unit': '', 'ref': ''},
            'C2': {'value': np.nan, 'unit': '', 'ref': ''},
            'C3': {'value': np.nan, 'unit': '', 'ref': ''},
            'C4+': {'value': np.nan, 'unit': '', 'ref': ''},
            'H2S': {'value': np.nan, 'unit': '', 'ref': ''},
        }
        client.parse_llm_response(data)
        # show_resp(client.responses)
        # show_resp(client.failed_response)
        assert_succeed_responses(want, client.responses)

    def test_parse_production_practices(self):
        client = ParserClient(model='test_model', field_name='test_field', section='Production practices')
        data = '{Gas-to-oil ratio (GOR):not_mentioned}\n{Water-to-oil ratio (WOR):not_mentioned}\n{Water injection ratio:not_mentioned}\n{Gas lifting injection ratio:not_mentioned}\n{Gas flooding injection ratio:not_mentioned}\n{Flood gas:not_mentioned}\n{Fraction of CO2 breaking through to producers:not_mentioned}\n{Source of makeup CO2:not_mentioned}\n{Percentage of sequestration credit assigned to the oilfield:not_mentioned}\n{Steam-to-oil ratio (SOR):3.0@Reference page 6, "Huff and puff used in 1977-1982. Total number of wells treated: 94, average number of cycles: 4. Additional oil production: 0.75 MMtons. SOR: 0.61."}\n{Fraction of required fossil electricity generated onsite:not_mentioned}\n{Fraction of remaining natural gas reinjected:not_mentioned}\n{Fraction of produced water reinjected:not_mentioned}\n{Fraction of steam generation via cogeneration:not_mentioned}\n{Fraction of steam generation via solar thermal:not_mentioned}'
        want = {
            'Gas-to-oil ratio (GOR)': {'value': np.nan, 'unit': '', 'ref': ''},
            'Water-to-oil ratio (WOR)': {'value': np.nan, 'unit': '', 'ref': ''},
            'Water injection ratio': {'value': np.nan, 'unit': '', 'ref': ''},
            'Gas lifting injection ratio': {'value': np.nan, 'unit': '', 'ref': ''},
            'Gas flooding injection ratio': {'value': np.nan, 'unit': '', 'ref': ''},
            'Flood gas': {'value': np.nan, 'unit': '', 'ref': ''},
            'Fraction of CO2 breaking through to producers': {'value': np.nan, 'unit': '', 'ref': ''},
            'Source of makeup CO2': {'value': np.nan, 'unit': '', 'ref': ''},
            'Steam-to-oil ratio (SOR)': {'value': np.nan, 'unit': '', 'ref': ''},
            'Fraction of required fossil electricity generated onsite': {'value': np.nan, 'unit': '', 'ref': ''},
            'Fraction of remaining natural gas reinjected': {'value': np.nan, 'unit': '', 'ref': ''},
            'Fraction of produced water reinjected': {'value': np.nan, 'unit': '', 'ref': ''},
            'Fraction of steam generation via cogeneration': {'value': np.nan, 'unit': '', 'ref': ''},
            'Fraction of steam generation via solar thermal': {'value': np.nan, 'unit': '', 'ref': ''},
        }
        client.parse_llm_response(data)
        show_resp(client.responses)
        # show_resp(client.failed_response)
        assert_succeed_responses(want, client.responses)

    def test_parse_crude_oil_transport(self):
        client = ParserClient(model='test_model', field_name='test_field', section='Crude oil transport')
        data = '{Ocean tanker:not_mentioned}\n{Barge:not_mentioned}\n{Pipeline:not_mentioned}\n{Rail:not_mentioned}\n{Truck:not_mentioned}\n{td_Ocean tanker:not_mentioned}\n{td_Barge:not_mentioned}\n{td_Pipeline:not_mentioned}\n{td_Rail:not_mentioned}\n{td_Truck:not_mentioned}\n{Ocean tanker size, if applicable:not_mentioned}'
        want = {
            'Ocean tanker': {'value': np.nan, 'unit': '', 'ref': ''},
            'Barge': {'value': np.nan, 'unit': '', 'ref': ''},
            'Pipeline': {'value': np.nan, 'unit': '', 'ref': ''},
            'Rail': {'value': np.nan, 'unit': '', 'ref': ''},
            'Truck': {'value': np.nan, 'unit': '', 'ref': ''},
            'td_Ocean tanker': {'value': np.nan, 'unit': '', 'ref': ''},
            'td_Barge': {'value': np.nan, 'unit': '', 'ref': ''},
            'td_Pipeline': {'value': np.nan, 'unit': '', 'ref': ''},
            'td_Rail': {'value': np.nan, 'unit': '', 'ref': ''},
            'td_Truck': {'value': np.nan, 'unit': '', 'ref': ''},
            'Ocean tanker size, if applicable': {'value': np.nan, 'unit': '', 'ref': ''},
        }
        client.parse_llm_response(data)
        # show_resp(client.responses)
        # show_resp(client.failed_response)
        assert_succeed_responses(want, client.responses)


class TestParserFindVariable(TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_find_variable(self):
        client = ParserClient(model='test_model', field_name='test_field', section='Fluid properties')
        var = client.find_variable('CO2')
        print(var)

