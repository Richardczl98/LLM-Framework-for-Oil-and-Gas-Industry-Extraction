# -*- coding: utf-8 -*-
# Author: Anjing Wang
# Date: Feb-01-2024

# reference
# https://docs.nlpcloud.com/?python#chatbot-and-conversational-ai
# https://github.com/nlpcloud/nlpcloud-python


import os
import sys
import time
import nlpcloud
from decouple import config
from ratelimit import limits, sleep_and_retry
from tenacity import retry, stop_after_attempt, retry_if_exception_type
import requests

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')
from model import tokens
from lib import helper
from model import models
import model.prompt_template as pt
from lib.my_logger import logger


MAXIMUM_RETRY_NUMBER = 5


class NLPCloudClient:
    ''' client for nlp cloud model'''
    _instance = None  # holds the unique instance
    _client_llama2 = None
    _client_chatdolphin = None
    _call_counter = 0

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
            cls._instance = super(NLPCloudClient, cls).__new__(cls)
            cls._instance._client_llama2 = None
            cls._instance._client_chatdolphin = None
        return cls._instance

    def _init_client(self) -> bool:
        # make sure the client is initialized only once
        if self._client_llama2:
            return True

        api_key = config("NLP_CLOUD_API_KEY", default=None)
        if api_key is None:
            return False

        self._client_llama2 = nlpcloud.Client(model=models.MDL_NLPC_LLAMA2,
                                              token=api_key,
                                              gpu=True)
        self._client_chatdolphin = nlpcloud.Client(models.MDL_NLPC_CDOLPHIN,
                                              token=api_key,
                                              gpu=True)

        return True

    @retry(stop=stop_after_attempt(MAXIMUM_RETRY_NUMBER),
           retry=retry_if_exception_type(Exception))
    def chat_single_turn(self,
                         usr_msg: str,
                         model: str = models.MDL_NLPC_LLAMA2,
                         sys_msg:str = pt.SYS_MSG_EXTRACTOR) -> str:
        """
        Generates a single turn chat response using the specified model.
        """
        if models.is_model_nlpcloud(model) is False:
            return f'{model} not supported yet.'

        if self._init_client() is False:
            return 'Failed to initialize client'

        if model == models.MDL_NLPC_LLAMA2:
            client = self._client_llama2
        elif model == models.MDL_NLPC_CDOLPHIN:
            client = self._client_chatdolphin

        self._call_counter += 1
        usr_msg_token_len = tokens.count_tokens(model, usr_msg)
        logger.debug('model: %s, usr_msg_token_len %s call_counter: %s',
                model, usr_msg_token_len,
                self._call_counter)
        try:
            resp = client.chatbot(usr_msg, context=sys_msg, history=[])
            logger.debug('model: %s, usr_msg_token_len %s call_counter: %s, resp: %s',
                        model, usr_msg_token_len,
                        self._call_counter, resp)
            return resp.get('response', '')
        except requests.exceptions.HTTPError as e:
            logger.error(e)
            return 'Fatal HTTP error. Check API error log.'


# for export
nlp_cloud_client = NLPCloudClient()


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
    ret = nlp_cloud_client.chat_single_turn('what is your version?',
                                             model=models.MDL_NLPC_LLAMA2)
    print(ret)


if __name__ == "__main__":
    main()
