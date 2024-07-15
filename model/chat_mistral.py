# -*- coding: utf-8 -*-
# Author: Anjing Wang
# Date: Feb-21-2024

# reference
# https://docs.mistral.ai/models/
# https://docs.mistral.ai/platform/client/


import os
import sys
import time
from decouple import config
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')
from lib import file_op
from lib import helper
from model import models
import model.prompt_template as pt
from lib.my_logger import logger
from tenacity import retry, stop_after_attempt, retry_if_exception_type


MAXIMUM_RETRY_NUMBER = 5


class MyMistralClient:
    ''' client for mistral model'''
    _instance = None  # holds the unique instance
    _client = None
    _inited = False
    _call_counter = 0
    _no_of_tokens_prompt = {models.MDL_MISTRAL_7B: 0,
                            models.MDL_MISTRAL_8X7B: 0,
                            models.MDL_MISTRAL_SMALL: 0,
                            models.MDL_MISTRAL_MEDIUM: 0,
                            models.MDL_MISTRAL_LARGE: 0}
    _no_of_tokens_completion = {models.MDL_MISTRAL_7B: 0,
                                models.MDL_MISTRAL_8X7B: 0,
                                models.MDL_MISTRAL_SMALL: 0,
                                models.MDL_MISTRAL_MEDIUM: 0,
                                models.MDL_MISTRAL_LARGE: 0}


    def __new__(cls):
        """
        Standard singleton design pattern.
        Initializes and returns an instance of the AnthropicClient class
        only if it doesn't already exist.

        Parameters:
            cls (type): The class object.

        Returns:
            AnthropicClient: The instance of the AnthropicClient class.
        """
        if cls._instance is None:
            cls._instance = super(MyMistralClient, cls).__new__(cls)
        return cls._instance

    def _init_client(self) -> bool:
        if self._inited:
            return True

        api_key = config("MISTRAL_API_KEY", default=None)
        if api_key is None:
            return False

        self._client = MistralClient(api_key=api_key)
        self._inited = True

        return True

    def _count_tokens(self, model, prompt_tokens, completion_tokens):
        if model == models.MDL_MISTRAL_7B:
            self._no_of_tokens_prompt[models.MDL_MISTRAL_7B] += \
                prompt_tokens
            self._no_of_tokens_completion[models.MDL_MISTRAL_7B] += \
                completion_tokens
        elif model == models.MDL_MISTRAL_8X7B:
            self._no_of_tokens_prompt[models.MDL_MISTRAL_8X7B] += \
                prompt_tokens
            self._no_of_tokens_completion[models.MDL_MISTRAL_8X7B] += \
                completion_tokens
        elif model == models.MDL_MISTRAL_SMALL:
            self._no_of_tokens_prompt[models.MDL_MISTRAL_SMALL] += \
                prompt_tokens
            self._no_of_tokens_completion[models.MDL_MISTRAL_SMALL] += \
                completion_tokens
        elif model == models.MDL_MISTRAL_MEDIUM:
            self._no_of_tokens_prompt[models.MDL_MISTRAL_MEDIUM] += \
                prompt_tokens
            self._no_of_tokens_completion[models.MDL_MISTRAL_MEDIUM] += \
                completion_tokens
        elif model == models.MDL_MISTRAL_LARGE:
            self._no_of_tokens_prompt[models.MDL_MISTRAL_LARGE] += \
                prompt_tokens
            self._no_of_tokens_completion[models.MDL_MISTRAL_LARGE] += \
                completion_tokens

    def get_current_cost(self):
        """
        Get the current cost of the mistral API.
        """
        # azure and openai pricing is the same
        # https://azure.microsoft.com/en-gb/pricing/details/cognitive-services/openai-service/
        # https://openai.com/pricing
        # GPT-3.5-Turbo-1106 16K has the best price
        cost = self._no_of_tokens_prompt[models.MDL_MISTRAL_7B] * 0.25 / 1000000 + \
               self._no_of_tokens_completion[models.MDL_MISTRAL_7B] * 0.25 / 1000000 + \
               self._no_of_tokens_prompt[models.MDL_MISTRAL_8X7B] * 0.7 / 1000000 + \
               self._no_of_tokens_completion[models.MDL_MISTRAL_8X7B] * 0.7 / 1000000 + \
               self._no_of_tokens_prompt[models.MDL_MISTRAL_SMALL] * 2 / 1000000 + \
               self._no_of_tokens_completion[models.MDL_MISTRAL_SMALL] * 6 / 1000000 + \
               self._no_of_tokens_prompt[models.MDL_MISTRAL_MEDIUM] * 2.7 / 1000000 + \
               self._no_of_tokens_completion[models.MDL_MISTRAL_MEDIUM] * 8.1 / 1000000 + \
               self._no_of_tokens_prompt[models.MDL_MISTRAL_LARGE] * 8 / 1000000 + \
               self._no_of_tokens_completion[models.MDL_MISTRAL_LARGE] * 24 / 1000000

        return cost

    def save_cost_to_file(self, filename: str):
        """
        Save the cost of the prompt, completion, and the total cost to a file.
        """
        file_op.save_dict_to_json(self.get_stats(), filename)

    def get_stats(self):
        """return a dictionary containing the stat"""
        dict_stats = {}
        dict_stats['no_of_tokens_prompt'] = self._no_of_tokens_prompt
        dict_stats['no_of_tokens_completion'] = self._no_of_tokens_completion
        dict_stats['cost'] = self.get_current_cost()
        logger.info(dict_stats)
        return dict_stats


    @retry(stop=stop_after_attempt(MAXIMUM_RETRY_NUMBER),
           retry=retry_if_exception_type(Exception))
    def chat_single_turn(self,
                         usr_msg: str,
                         model: str = models.MDL_MISTRAL_SMALL,
                         sys_msg:str = pt.SYS_MSG_EXTRACTOR) -> str:
        """
        Generates a single turn chat response using the specified model.
        """
        if models.is_model_mistral(model) is False:
            return f'{model} not supported yet.'

        if self._init_client() is False:
            return 'Failed to initialize client'

        self._call_counter += 1

        # https://docs.mistral.ai/api/#operation/createChatCompletion
        messages = [
            ChatMessage(role="system", content=sys_msg),
            ChatMessage(role="user", content=usr_msg)
        ]
        resp = self._client.chat(
            model = model,
            messages = messages
        )
        logger.debug('model: %s, call_counter: %s, resp: %s',
                     model, self._call_counter, resp)

        self._count_tokens(
            model = model,
            prompt_tokens = resp.usage.prompt_tokens,
            completion_tokens = resp.usage.completion_tokens
        )

        resp_txt = resp.choices[0].message.content

        return resp_txt


# for export
mistral_client = MyMistralClient()


def main():
    """
    This is the main function of the program.
    """
    # print(chat_single_turn('hello world! what is your name?'))
    # chat_interactive()
    # print(anthropic_get_api_key(True))
    # print(chat_single_turn("讲一个笑话"))
    # print(chat_single_turn("what is your name?"))
    # Usage:
    ret = mistral_client.chat_single_turn('who are you?')
    print(ret)
    cost = mistral_client.get_current_cost()
    print(cost)


if __name__ == "__main__":
    main()
