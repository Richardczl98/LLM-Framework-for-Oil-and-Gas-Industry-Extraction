import unittest

from eval.parser.parser_unit import ParserUnit


class TestParserUnit(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_parser_unit(self):
        data = '32°API@The reservoirs contain 32°API crude with solution GOR of 540 scf/stb. All reservoirs have primary gas caps, with saturation pressures between 180 and 220 bars.'
        result = ParserUnit().parse(data, unit='deg.API')
        print(result.data)

    def test_parse_water_to_oil_ratio(self):
        data = '15.5@Page 5, "Water/oil ratio, 15.5"'
        result = ParserUnit().parse(data, unit='bbl water/bbl oil')
        print(result)

    def test_parse_gas_to_oil_ratio(self):
        data = 'not_mentioned'
        result = ParserUnit().parse(data, unit='bbl water/bbl oil')
        print(result)


class TestParserUnitV2(unittest.TestCase):
    def test_parser_unit(self):
        import numpy as np
        data = [
            "150 - 900 mD@Reference page 4: 'Permeability (mD) ,> 100 ,100 ,150 - 900'"]
        for item in data:
            rst = ParserUnit().parse(item, unit="mD")
            assert None == rst.error
            assert 525 == rst.data.value

        data = [
            '200° F  @Page 3, "The NWFB injection began with clean 80° F seawater, '
            'then changed to 160° F produced water with small amounts of oil and solids."'
        ]
        for item in data:
            rst = ParserUnit().parse(item, unit="°f")
            assert None == rst.error
            assert 200 == rst.data.value

        data = [
            "'18º API@ The Lagunillas 07 reservoir is located Lake Maracaibo in Venezuela...The oil had an 18º API and a 'viscosity of 21 cp at initial conditions'"
        ]
        for item in data:
            rst = ParserUnit().parse(item, unit="deg.api")
            assert None == rst.error
            assert 18 == rst.data.value

        data = [
            '"32°API  @Reference page 2 and content: "The reservoirs contain 32°API crude with solution GOR of 540 scf/stb."']
        for item in data:
            rst = ParserUnit().parse(item, unit="deg.api")
            assert 32.0 == rst.data.value
            assert None == rst.error

        data = [
            '1,200 to 2,900a ft subsurface @Page 1 - "The average depth of the sands ranges from 1,200 to 2,900 ft (365 to 844 m) subsurface.',
            '17 million barrels from 1984 to 1999, 160 million barrels expected if the flank waterflooding continues until 2019@The paper concludes...from 1984 to 1999. A net oil recovery of 160 million barrels is expected...until 2019',
            'Increased from 753 psia in 1984 to 950 psia in 1999 due to water injection@The average reservoir pressure increased from 753 psia in 1984 to 950 psia in 1999 in response to the water injection']

        unit = ['ft', 'barrels', 'psia']
        for idx in range(len(data)):
            rst = ParserUnit().parse(data[idx], unit=unit[idx])
            print(rst.data)
            print(rst.error)
            print(rst.data.value)

        data = [
            '22 deg API  @"The Haima West reservoir crude has high viscocity (90 cp) and moderate to low API gravity (22 deg API oil)." on page 1'
        ]
        for item in data:
            rst = ParserUnit().parse(item, unit="deg.api")
            assert 22 == rst.data.value
            assert None == rst.error

        data = ["32 degrees celsius"]
        for item in data:
            rst = ParserUnit().parse(item, unit="°f")
            assert 89.6 == rst.data.value
            assert None == rst.error

        data = ["12 degrees api"]
        for item in data:
            rst = ParserUnit().parse(item, unit="deg.api")
            assert 12 == rst.data.value
            assert None == rst.error

        data = ["77 water/oil-ratio"]
        for item in data:
            rst = ParserUnit().parse(item, unit='bbl water/bbl oil')
            assert 77 == rst.data.value
            assert None == rst.error

        data = ["77 bbl inj/bbl oil"]
        for item in data:
            rst = ParserUnit().parse(item, unit='bbl water/bbl oil')
            assert 77 == rst.data.value
            assert None == rst.error

        data = ["77 m3/ton"]
        for item in data:
            rst = ParserUnit().parse(item, unit='scf/bbl oil')
            assert 364.51 == rst.data.value
            assert None == rst.error

        data = ["Not mentioned", "not_mentioned", "not_mentioned"]
        for item in data:
            rst = ParserUnit().parse(item, unit='bbl water/bbl oil')
            assert rst.data.value is np.nan

        data = [
            "212-225 °F  @ | This is the end of page 8<This is the beginning of "
            "page 9 At Kem River producing well bottom hole temperatures may be in a range of 212-225 °F."]

        for item in data:
            rst = ParserUnit().parse(item, unit='°f')
            assert rst.data.value == 218.5

        data = [
            '1600-2100 meters  @Reference page 2 and content The Piltun field...at depths between 1600 and 2100 m subsea.']
        for item in data:
            rst = ParserUnit().parse(item, unit='ft')
            assert rst.data.value == 6068

        data = [
            '0.1-1.2 um2  @ | Reference page 7, "Okha5,18 (Sakhalin) ",1965-2006 ,500-700 ,Clastic 0.1-1.2 ,80-600 |  |  |  |  | ']
        for item in data:
            rst = ParserUnit().parse(item, unit='md')
            assert rst.data.value == 0.66

        data = ["3-1/2 or 2-7/8",
                '3-1/2” or 2-7/8”@Reference page and content',
                "3-1/2• or 2-7/8"]
        for item in data:
            rst = ParserUnit().parse(item, unit='ft',
                                     key='Injector tubing diameter')
            assert rst.data.value == 3.19

        data = '3.51%@on ofreservoir fluid: N2. 3.51%".51% @Reference page 3 and reference text "Composi'
        parse = ParserUnit().parse(data, unit='mol%')
        assert parse.data.value == 3.51

        data = '0.051 89 mole fraction@Page 2, "Table '
        parse = ParserUnit().parse(data, unit='mol%')
        assert parse.data.value == 5.19

        data = '62 °C - 72 °C@Reference page 12 and content "The reservoir temperature of Jubarte ranges from 62 °C to 72 °C" | not_mentioned'
        parse = ParserUnit().parse(data, unit='°f')
        assert parse.data.value == 152.6

        data = '600 bar @Referencepage 3, "The Achimovformation is highly'
        parse = ParserUnit().parse(data, unit='psia')
        assert parse.data.value == 8700

        data = ('40 Mstb/d@After a short period of peak production of 40 Mstb/d '
                'in 1967, a decline in the total field production was observed')
        parse = ParserUnit().parse(data, unit='bbl/d')
        assert parse.data.value == 40000

        data = (
            '324½@This is the beginning of page 4 Although inflow and vertical lift per')
        parse = ParserUnit().parse(data, unit='in', key='Producer tubing diameter')
        assert parse.data.value == 324.5