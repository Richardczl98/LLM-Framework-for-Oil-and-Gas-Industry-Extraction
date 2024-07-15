import unittest
from eval.parser.llm_response import transform_list


openai_response = {
    "okha": [
        [
             '{Downhole pump:not_mentioned}\n{Water reinjection:not_mentioned}\n{Natural gas reinjection:not_mentioned}\n{Water flooding:not_mentioned}\n{Gas lifting:not_mentioned}\n{Gas flooding:not_mentioned}\n{Steam flooding:mentioned/Page 6/ "Okha5,18 (Sakhalin) ",1965-2006 ,500-700 ,Clastic 0.1-1.2 ,80-600 ,"Huff and puff in individual blocks of field started in 1962. Steam flooding in individual blocks was carried out from 1973 to 1987. Total injection: steam: 16.5 MMtons, water: 65.5 MMtons. Additional oil production: 5.6 MMtons (35.7 % total oil production). Steam oil ratio (SOR):  3.0"}\n{Oil sands mine (integrated with upgrader):not_mentioned}\n{Oil sands mine (non-integrated with upgrader):not_mentioned}',
             '{Downhole pump:not_mentioned}\n{Water reinjection:not_mentioned}\n{Natural gas reinjection:not_mentioned}\n{Water flooding:not_mentioned}\n{Gas lifting:not_mentioned}\n{Gas flooding:not_mentioned}\n{Steam flooding:not_mentioned}\n{Oil sands mine (integrated with upgrader):not_mentioned}\n{Oil sands mine (non-integrated with upgrader):not_mentioned}',
             '{Downhole pump:not_mentioned}\n{Water reinjection:not_mentioned}\n{Natural gas reinjection:not_mentioned}\n{Water flooding:not_mentioned}\n{Gas lifting:not_mentioned}\n{Gas flooding:not_mentioned}\n{Steam flooding:not_mentioned}\n{Oil sands mine (integrated with upgrader):not_mentioned}\n{Oil sands mine (non-integrated with upgrader):not_mentioned}'
        ],
        [
             '{Field location (Country): Sakhalin, Russia/Reference page 6}\n{Field age:not_mentioned}\n{Field depth:not_mentioned}\n{Oil production volume:not_mentioned}\n{Number of producing wells:not_mentioned}\n{Number of water injecting wells:not_mentioned}\n{Production tubing diameter:not_mentioned}\n{Productivity index:not_mentioned}\n{Reservoir pressure:not_mentioned}\n{Reservoir temperature:not_mentioned}\n{offshore:not_mentioned}',
             '{Field location (Country):not_mentioned}\n{Field age:not_mentioned}\n{Field depth:not_mentioned}\n{Oil production volume:not_mentioned}\n{Number of producing wells:not_mentioned}\n{Number of water injecting wells:not_mentioned}\n{Production tubing diameter:not_mentioned}\n{Productivity index:not_mentioned}\n{Reservoir pressure:not_mentioned}\n{Reservoir temperature:not_mentioned}\n{offshore:not_mentioned}',
             '{Field location (Country):not_mentioned}\n{Field age:not_mentioned}\n{Field depth:not_mentioned}\n{Oil production volume:not_mentioned}\n{Number of producing wells:not_mentioned}\n{Number of water injecting wells:not_mentioned}\n{Production tubing diameter:not_mentioned}\n{Productivity index:not_mentioned}\n{Reservoir pressure:not_mentioned}\n{Reservoir temperature:not_mentioned}\n{offshore:not_mentioned}'
        ],
    ],
    "usinskoe":[
        [
             '{Downhole pump:not_mentioned}\n{Water reinjection:not_mentioned}\n{Natural gas reinjection:not_mentioned}\n{Water flooding:not_mentioned}\n{Gas lifting:not_mentioned}\n{Gas flooding:not_mentioned}\n{Steam flooding:mentioned/Page 6, "Usinskoe4 (Komi, Timan Pechora) 1982-2006 +"and "Steam flooding: steam ring (0.6-0.8 PV- porous volume) pushed by cold water (1.7-1.9 PV)"}\n{Oil sands mine (integrated with upgrader):not_mentioned}\n{Oil sands mine (non-integrated with upgrader):not_mentioned}',
             '{Downhole pump:not_mentioned}\n{Water reinjection:not_mentioned}\n{Natural gas reinjection:not_mentioned}\n{Water flooding:not_mentioned}\n{Gas lifting:not_mentioned}\n{Gas flooding:not_mentioned}\n{Steam flooding:not_mentioned}\n{Oil sands mine (integrated with upgrader):not_mentioned}\n{Oil sands mine (non-integrated with upgrader):not_mentioned}',
             '{Downhole pump:not_mentioned}\n{Water reinjection:not_mentioned}\n{Natural gas reinjection:not_mentioned}\n{Water flooding:not_mentioned}\n{Gas lifting:not_mentioned}\n{Gas flooding:not_mentioned}\n{Steam flooding:not_mentioned}\n{Oil sands mine (integrated with upgrader):not_mentioned}\n{Oil sands mine (non-integrated with upgrader):not_mentioned}'
        ],
        [
             '{Field location (Country): Russia/Reference page 6 and content}\n{Field age:not_mentioned}\n{Field depth:not_mentioned}\n{Oil production volume:not_mentioned}\n{Number of producing wells:not_mentioned}\n{Number of water injecting wells:not_mentioned}\n{Production tubing diameter:not_mentioned}\n{Productivity index:not_mentioned}\n{Reservoir pressure:not_mentioned}\n{Reservoir temperature:not_mentioned}\n{offshore:not_mentioned}',
             '{Field location (Country):not_mentioned}\n{Field age:not_mentioned}\n{Field depth:not_mentioned}\n{Oil production volume:not_mentioned}\n{Number of producing wells:not_mentioned}\n{Number of water injecting wells:not_mentioned}\n{Production tubing diameter:not_mentioned}\n{Productivity index:not_mentioned}\n{Reservoir pressure:not_mentioned}\n{Reservoir temperature:not_mentioned}\n{offshore:not_mentioned}',
             '{Field location (Country):not_mentioned}\n{Field age:not_mentioned}\n{Field depth:not_mentioned}\n{Oil production volume:not_mentioned}\n{Number of producing wells:not_mentioned}\n{Number of water injecting wells:not_mentioned}\n{Production tubing diameter:not_mentioned}\n{Productivity index:not_mentioned}\n{Reservoir pressure:not_mentioned}\n{Reservoir temperature:not_mentioned}\n{offshore:not_mentioned}'
        ],
    ]

}


class LLMResponseTestCase(unittest.TestCase):
    def test_transform_list(self):
        want = [
            [
                '{Downhole pump:not_mentioned}\n{Water reinjection:not_mentioned}\n{Natural gas reinjection:not_mentioned}\n{Water flooding:not_mentioned}\n{Gas lifting:not_mentioned}\n{Gas flooding:not_mentioned}\n{Steam flooding:mentioned/Page 6/ "Okha5,18 (Sakhalin) ",1965-2006 ,500-700 ,Clastic 0.1-1.2 ,80-600 ,"Huff and puff in individual blocks of field started in 1962. Steam flooding in individual blocks was carried out from 1973 to 1987. Total injection: steam: 16.5 MMtons, water: 65.5 MMtons. Additional oil production: 5.6 MMtons (35.7 % total oil production). Steam oil ratio (SOR):  3.0"}\n{Oil sands mine (integrated with upgrader):not_mentioned}\n{Oil sands mine (non-integrated with upgrader):not_mentioned}',
                '{Field location (Country): Sakhalin, Russia/Reference page 6}\n{Field age:not_mentioned}\n{Field depth:not_mentioned}\n{Oil production volume:not_mentioned}\n{Number of producing wells:not_mentioned}\n{Number of water injecting wells:not_mentioned}\n{Production tubing diameter:not_mentioned}\n{Productivity index:not_mentioned}\n{Reservoir pressure:not_mentioned}\n{Reservoir temperature:not_mentioned}\n{offshore:not_mentioned}',

            ],
            [
                '{Downhole pump:not_mentioned}\n{Water reinjection:not_mentioned}\n{Natural gas reinjection:not_mentioned}\n{Water flooding:not_mentioned}\n{Gas lifting:not_mentioned}\n{Gas flooding:not_mentioned}\n{Steam flooding:not_mentioned}\n{Oil sands mine (integrated with upgrader):not_mentioned}\n{Oil sands mine (non-integrated with upgrader):not_mentioned}',
                '{Field location (Country):not_mentioned}\n{Field age:not_mentioned}\n{Field depth:not_mentioned}\n{Oil production volume:not_mentioned}\n{Number of producing wells:not_mentioned}\n{Number of water injecting wells:not_mentioned}\n{Production tubing diameter:not_mentioned}\n{Productivity index:not_mentioned}\n{Reservoir pressure:not_mentioned}\n{Reservoir temperature:not_mentioned}\n{offshore:not_mentioned}',
            ],
            [
                '{Downhole pump:not_mentioned}\n{Water reinjection:not_mentioned}\n{Natural gas reinjection:not_mentioned}\n{Water flooding:not_mentioned}\n{Gas lifting:not_mentioned}\n{Gas flooding:not_mentioned}\n{Steam flooding:not_mentioned}\n{Oil sands mine (integrated with upgrader):not_mentioned}\n{Oil sands mine (non-integrated with upgrader):not_mentioned}',
                '{Field location (Country):not_mentioned}\n{Field age:not_mentioned}\n{Field depth:not_mentioned}\n{Oil production volume:not_mentioned}\n{Number of producing wells:not_mentioned}\n{Number of water injecting wells:not_mentioned}\n{Production tubing diameter:not_mentioned}\n{Productivity index:not_mentioned}\n{Reservoir pressure:not_mentioned}\n{Reservoir temperature:not_mentioned}\n{offshore:not_mentioned}',
            ],
        ]
        assert want == transform_list(openai_response['okha'])

