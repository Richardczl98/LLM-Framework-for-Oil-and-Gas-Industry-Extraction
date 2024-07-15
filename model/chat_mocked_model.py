# -*- coding: utf-8 -*-
# Author: Carvin Li


import os
import sys
from pathlib import Path
import json
import traceback

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')

from lib.my_logger import logger


class MockedLLMClient:
    def __init__(self):
        self.data = {}

    def chat_single_turn(self, usr_msg: str) -> str:
        """
        Generates a single turn chat response using the specified model.
        """
        try:
            answer = self.data[usr_msg]
        except KeyError as err:
            logger.exception(err)
            logger.exception(traceback.format_exc())
            answer = ''

        return answer

    def update(self, prompt: str, answer: str):
        self.data.update({prompt: answer})

    def load(self, file_path: str | Path):
        with open(file_path, 'r') as file:
            self.data = json.load(file)

    def dump(self, file_path: str | Path):
        with open(file_path, 'w') as file:
            json.dump(self.data, fp=file)


mocked_llm_client = MockedLLMClient()
