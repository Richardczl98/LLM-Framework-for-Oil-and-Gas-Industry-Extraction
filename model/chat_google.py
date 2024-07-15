# -*- coding: utf-8 -*-
# Author: Anjing Wang
# Date: Feb-01-2024

# reference
# https://docs.nlpcloud.com/?python#chatbot-and-conversational-ai
# https://github.com/nlpcloud/nlpcloud-python


import os
import sys
import time
from decouple import config
import google.generativeai as genai

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')
from lib import helper
from model import models
import model.prompt_template as pt
from lib.my_logger import logger
from tenacity import retry, stop_after_attempt, retry_if_exception_type


MAXIMUM_RETRY_NUMBER = 5


class GoogleAIClient:
    ''' client for nlp cloud model'''
    _instance = None  # holds the unique instance
    _inited = False
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
            cls._instance = super(GoogleAIClient, cls).__new__(cls)
        return cls._instance

    def _init_client(self) -> bool:
        if self._inited:
            return True

        api_key = config("GOOGLE_API_KEY", default=None)
        if api_key is None:
            return False

        genai.configure(api_key=api_key)
        self._inited = True

        return True

    @retry(stop=stop_after_attempt(MAXIMUM_RETRY_NUMBER),
           retry=retry_if_exception_type(Exception))
    def chat_single_turn(self,
                         usr_msg: str,
                         model: str = models.MDL_GOOG_GEMINI_PRO,
                         sys_msg:str = pt.SYS_MSG_EXTRACTOR) -> str:
        """
        Generates a single turn chat response using the specified model.
        """
        if models.is_model_google(model) is False:
            return f'{model} not supported yet.'

        if self._init_client() is False:
            return 'Failed to initialize client'

        client = genai.GenerativeModel(model)
        self._call_counter += 1
        prompt = (
            f'context: {sys_msg}'
            f'{usr_msg}'
        )
        resp = client.generate_content(prompt)
        logger.debug('model: %s, call_counter: %s, resp: %s',
                     model, self._call_counter, resp)
        # sleep long enough to be within the rate limit
        # the current rate limit is 2 requests per minute
        time.sleep(31)

        resp_text = ''
        try:
            # resp_text = resp.text
            # always use full accessor instead of above quick accessor
            resp_text =  resp.candidates[0].content.parts[0].text
        except Exception as e:
            logger.error('Do not contain a valid response. ValueError: %s', e)

        return resp_text

    def list_models(self):
        """
        List all available models.
        """
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)


# for export
google_ai_client = GoogleAIClient()


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
    ret = google_ai_client.chat_single_turn('who are you?',
                                              model='gemini-1.5-pro-latest')

    print(ret)
    # import pprint
    # for model in genai.list_models():
    #     if 'generateContent' in model.supported_generation_methods:
    #         print(model.name)
    #         # pprint.pprint(model)

    # google_ai_client.list_models()


if __name__ == "__main__":
    main()
