import unittest
from collections import OrderedDict
import numpy as np

from eval.xls_parser import ParseExcel
from converter.dict2xls import convert_dict_to_dataframe


class TestDict2Xls(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_convert_dict_to_df(self):
        data = {'fields': ['okha', 'usinskoe'], 'okha': OrderedDict([('downhole pump', [np.nan, '', '', 'not_mentioned']), ('water reinjection', [np.nan, '', '', 'not_mentioned']), ('natural gas reinjection', [np.nan, '', '', 'not_mentioned']), ('water flooding', [np.nan, '', '', 'not_mentioned']), ('gas lifting', [np.nan, '', '', 'not_mentioned']), ('gas flooding', [np.nan, '', '', 'not_mentioned']), ('steam flooding', [1.0, '', 'Reference page and content: "Okha5,18 (Sakhalin)", 1965-2006, Steam flooding in individual blocks was carried out from 1973 to 1987. Additional oil production: 5.6 MMtons |  |  |  | ', 'not_mentioned | mentioned@Reference page and content: "Okha5,18 (Sakhalin)", 1965-2006, Steam flooding in individual blocks was carried out from 1973 to 1987. Additional oil production: 5.6 MMtons | not_mentioned | not_mentioned | not_mentioned | not_mentioned']), ('oil sands mine (integrated with upgrader)', [np.nan, '', '', 'not_mentioned']), ('oil sands mine (non-integrated with upgrader)', [np.nan, '', '', 'not_mentioned']), ('field location (country)', ['Sakhalin, Russia', '', ' | Page 7, "Okha5,18 (Sakhalin)" |  |  |  | ', 'not_mentioned | Sakhalin, Russia@Page 7, "Okha5,18 (Sakhalin)" | not_mentioned | not_mentioned | not_mentioned | not_mentioned']), ('field age', [np.nan, '', '', 'not_mentioned']), ('field depth', [np.nan, '', '', 'not_mentioned']), ('oil production volume', [np.nan, '', '', 'not_mentioned']), ('number of producing wells', [np.nan, '', '', 'not_mentioned']), ('number of water injecting wells', [np.nan, '', '', 'not_mentioned']), ('production tubing diameter', [np.nan, '', '', 'not_mentioned']), ('productivity index', [np.nan, '', '', 'not_mentioned']), ('reservoir pressure', [np.nan, '', '', 'not_mentioned']), ('reservoir temperature', [np.nan, '', '', 'not_mentioned']), ('offshore', [np.nan, '', '', 'not_mentioned']), ('api gravity (oil at standard pressure and temperature, or "dead oil")', [np.nan, '', '', 'not_mentioned']), ('n2', [np.nan, '', '', 'not_mentioned']), ('co2', [np.nan, '', '', 'not_mentioned']), ('c1', [np.nan, '', '', 'not_mentioned']), ('c2', [np.nan, '', '', 'not_mentioned']), ('c3', [np.nan, '', '', 'not_mentioned']), ('c4+', [np.nan, '', '', 'not_mentioned']), ('h2s', [np.nan, '', '', 'not_mentioned']), ('gas-to-oil ratio (gor)', [np.nan, '', '', 'not_mentioned']), ('water-to-oil ratio (wor)', [np.nan, '', '', 'not_mentioned']), ('water injection ratio', [np.nan, '', '', 'not_mentioned']), ('gas lifting injection ratio', [np.nan, '', '', 'not_mentioned']), ('gas flooding injection ratio', [np.nan, '', '', 'not_mentioned']), ('flood gas', [np.nan, '', '', 'not_mentioned']), ('fraction of co2 breaking through to producers', [np.nan, '', '', 'not_mentioned']), ('source of makeup co2', [np.nan, '', '', 'not_mentioned']), ('percentage of sequestration credit assigned to the oilfield', [np.nan, '', '', 'not_mentioned']), ('steam-to-oil ratio (sor)', [np.nan, '', '', 'not_mentioned']), ('fraction of required fossil electricity generated onsite', [np.nan, '', '', 'not_mentioned']), ('fraction of remaining natural gas reinjected', [np.nan, '', '', 'not_mentioned']), ('fraction of produced water reinjected', [np.nan, '', '', 'not_mentioned']), ('fraction of steam generation via cogeneration', [np.nan, '', '', 'not_mentioned']), ('fraction of steam generation via solar thermal', [np.nan, '', '', 'not_mentioned']), ('heater/treater', [np.nan, '', '', 'not_mentioned']), ('stabilizer column', [np.nan, '', '', 'not_mentioned']), ('upgrader type', [np.nan, '', '', 'not_mentioned']), ('associated gas processing path', [np.nan, '', '', 'not_mentioned']), ('flaring-to-oil ratio', [np.nan, '', '', 'not_mentioned']), ('purposeful venting fraction (post-flare gas fraction vented)', [np.nan, '', '', 'not_mentioned']), ('volume fraction of diluent', [np.nan, '', '', 'not_mentioned']), ('small sources emissions', [np.nan, '', '', 'not_mentioned'])]), 'usinskoe': OrderedDict([('downhole pump', [np.nan, '', '', 'not_mentioned']), ('water reinjection', [np.nan, '', '', 'not_mentioned']), ('natural gas reinjection', [np.nan, '', '', 'not_mentioned']), ('water flooding', [np.nan, '', '', 'not_mentioned']), ('gas lifting', [np.nan, '', '', 'not_mentioned']), ('gas flooding', [np.nan, '', '', 'not_mentioned']), ('steam flooding', [1.0, '', ' | Page 6, "Steam flooding was started on small area (~10 % of field) in 1982-1993. Total injection: steam - 10 MMtons, water- 22.9 MMtons. Additional oil production: 9 MMtons" |  |  |  | ', 'not_mentioned | mentioned@Page 6, "Steam flooding was started on small area (~10 % of field) in 1982-1993. Total injection: steam - 10 MMtons, water- 22.9 MMtons. Additional oil production: 9 MMtons" | not_mentioned | not_mentioned | not_mentioned | not_mentioned']), ('oil sands mine (integrated with upgrader)', [np.nan, '', '', 'not_mentioned']), ('oil sands mine (non-integrated with upgrader)', [np.nan, '', '', 'not_mentioned']), ('field location (country)', [np.nan, '', '', 'not_mentioned']), ('field age', [np.nan, '', '', 'not_mentioned']), ('field depth', [np.nan, '', '', 'not_mentioned']), ('oil production volume', [np.nan, '', '', 'not_mentioned']), ('number of producing wells', [np.nan, '', '', 'not_mentioned']), ('number of water injecting wells', [np.nan, '', '', 'not_mentioned']), ('production tubing diameter', [np.nan, '', '', 'not_mentioned']), ('productivity index', [np.nan, '', '', 'not_mentioned']), ('reservoir pressure', [np.nan, '', '', 'not_mentioned']), ('reservoir temperature', [np.nan, '', '', 'not_mentioned']), ('offshore', [np.nan, '', '', 'not_mentioned']), ('api gravity (oil at standard pressure and temperature, or "dead oil")', [np.nan, '', '', 'not_mentioned']), ('n2', [np.nan, '', '', 'not_mentioned']), ('co2', [np.nan, '', '', 'not_mentioned']), ('c1', [np.nan, '', '', 'not_mentioned']), ('c2', [np.nan, '', '', 'not_mentioned']), ('c3', [np.nan, '', '', 'not_mentioned']), ('c4+', [np.nan, '', '', 'not_mentioned']), ('h2s', [np.nan, '', '', 'not_mentioned']), ('gas-to-oil ratio (gor)', [np.nan, '', '', 'not_mentioned']), ('water-to-oil ratio (wor)', [np.nan, '', '', 'not_mentioned']), ('water injection ratio', [np.nan, '', '', 'not_mentioned']), ('gas lifting injection ratio', [np.nan, '', '', 'not_mentioned']), ('gas flooding injection ratio', [np.nan, '', '', 'not_mentioned']), ('flood gas', [np.nan, '', '', 'not_mentioned']), ('fraction of co2 breaking through to producers', [np.nan, '', '', 'not_mentioned']), ('source of makeup co2', [np.nan, '', '', 'not_mentioned']), ('percentage of sequestration credit assigned to the oilfield', [np.nan, '', '', 'not_mentioned']), ('steam-to-oil ratio (sor)', [np.nan, '', '', 'not_mentioned']), ('fraction of required fossil electricity generated onsite', [np.nan, '', '', 'not_mentioned']), ('fraction of remaining natural gas reinjected', [np.nan, '', '', 'not_mentioned']), ('fraction of produced water reinjected', [np.nan, '', '', 'not_mentioned']), ('fraction of steam generation via cogeneration', [np.nan, '', '', 'not_mentioned']), ('fraction of steam generation via solar thermal', [np.nan, '', '', 'not_mentioned']), ('heater/treater', [np.nan, '', '', 'not_mentioned']), ('stabilizer column', [np.nan, '', '', 'not_mentioned']), ('upgrader type', [np.nan, '', '', 'not_mentioned']), ('associated gas processing path', [np.nan, '', '', 'not_mentioned']), ('flaring-to-oil ratio', [np.nan, '', '', 'not_mentioned']), ('purposeful venting fraction (post-flare gas fraction vented)', [np.nan, '', '', 'not_mentioned']), ('volume fraction of diluent', [np.nan, '', '', 'not_mentioned']), ('small sources emissions', [np.nan, '', '', 'not_mentioned'])])}
        got = convert_dict_to_dataframe(data, mode='ref')
        print(got)