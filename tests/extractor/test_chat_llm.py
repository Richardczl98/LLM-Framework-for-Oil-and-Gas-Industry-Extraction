import unittest
from pathlib import Path

from extractor.chat_llm import ask_llm_is_same_country


class TestAskSameCountry(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_ask_Moscow_Russia(self):
        c1 = 'Moscow'
        c2 = 'Russia'

        got = ask_llm_is_same_country(c1, c2)

        assert got is True

    def test_ask_Africa_South_Africa(self):
        c1 = 'Kazakhstan'
        c2 = 'Soviet Union'

        got = ask_llm_is_same_country(c1, c2)

        assert got is True
