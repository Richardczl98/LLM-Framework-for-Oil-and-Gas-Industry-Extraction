# -*- coding: utf-8 -*-
# Author: Anjing Wang

# reference
# https://github.com/anthropics/anthropic-sdk-python


import os
import sys
from decouple import config
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')

from lib import helper
from model import models, tokens
import model.prompt_template as pt
from lib.my_logger import logger
from lib import file_op


class AnthropicClient:
    ''' client for Claude model'''
    _instance = None  # holds the unique instance
    _client_anthropic = None
    _no_of_tokens_input = 0
    _no_of_tokens_output = 0

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
            cls._instance = super(AnthropicClient, cls).__new__(cls)
            cls._instance.client_anthropic = None
        return cls._instance

    def _init_client(self) -> bool:
        # make sure the client is initialized only once
        if self._client_anthropic:
            return True

        api_key = config("ANTHROPIC_API_KEY", default=None)
        if api_key is None:
            return False

        # client has a default retry of 2, unless overridden by max_retries
        self._client_anthropic = Anthropic(api_key=api_key)

        self._no_of_tokens_input = 0
        self._no_of_tokens_output = 0
        return True

    def chat_single_turn(self,
                         usr_msg: str,
                         model: str = models.MDL_CLAUDE_3_OPUS,
                         sys_msg:str = pt.SYS_MSG_EXTRACTOR) -> str:
        """
        Generates a single turn chat response using the specified model.

        Args:
            usr_msg (str): The user message to be used as input for the chat.
            model (str, optional): The model to be used for generating the chat response.
                                   Defaults to 'claude-2'.

        Returns:
            str: The generated chat response.

        Raises:
            Exception: If there is an error calling the Anthropic API.
        """
        if models.is_model_anthropic(model) is False:
            return f'{model} not supported yet.'

        if self._init_client() is False:
            return 'Failed to initialize client'

        # claude-2 should automatically use latest version 2.1
        # but we recommend to call directly with the latest version
        # which uses the new style of the API
        if model == models.MDL_CLAUDE_2:
            logger.info('Using old style Claude API text prompt completion')
            # https://docs.anthropic.com/claude/reference/complete_post
            # {HUMAN_PROMPT} {AI_PROMPT} is the old style
            # With Text Completions, the system prompt is specified by adding text before the first \n\nHuman:
            msgs = f"{sys_msg}\n{HUMAN_PROMPT}{usr_msg}{AI_PROMPT}"

            try:
                response = self._client_anthropic.completions.create(
                    model=models.MDL_CLAUDE_2,
                    max_tokens_to_sample=tokens.TOKEN_OUTPUT_FOR_SECTION,
                    prompt=msgs,
                    temperature=0.6
                )
                return response.completion
            except Exception as e:
                print(f"Error calling the Anthropic API: {e}")
                return ''
        else:
            logger.info('Using v2 style Claude API messages')
            # https://docs.anthropic.com/claude/reference/migrating-from-text-completions-to-messages
            try:
                response = self._client_anthropic.messages.create(
                    model=models.MDL_CLAUDE_3_OPUS,
                    # claude has enough windows, so we increase it by 1000
                    max_tokens=tokens.TOKEN_OUTPUT_FOR_SECTION+1000,
                    # we use the same temperature as gpt-4
                    # but this needs to be tested
                    temperature=0.6,
                    system=sys_msg,
                    messages=[
                        {"role": "user", "content": usr_msg} # <-- user prompt
                    ]
                )
                # https://docs.anthropic.com/claude/reference/migrating-from-text-completions-to-messages
                # During the beta, response content will only have one block, and it will be of type text.
                input_tokens =  response.usage.input_tokens
                output_tokens = response.usage.output_tokens
                self._no_of_tokens_input += input_tokens
                self._no_of_tokens_output += output_tokens
                return response.content[0].text
            except Exception as e:
                print(f"Error calling the Anthropic API: {e}")
                return ''

    def get_current_cost(self):
        """
        Get the current cost of the claude API.
        """
        # https://www-cdn.anthropic.com/files/4zrzovbb/website/31021aea87c30ccaecbd2e966e49a03834bfd1d2.pdf
        # input $8/million token output $24/million
        # write it as / k to compare with GPT
        # Mar-2024, claude 3 price 
        # https://www.anthropic.com/api#pricing
        cost = self._no_of_tokens_input * 0.008 / 1000 + \
               self._no_of_tokens_output * 0.024 / 1000
        return cost

    def get_stats(self):
        """return a dictionary containing the stat"""
        dict_stats = {}
        dict_stats['no_of_tokens_prompt'] = self._no_of_tokens_input
        dict_stats['no_of_tokens_completion'] = self._no_of_tokens_output
        dict_stats['cost'] = self.get_current_cost()
        logger.info(dict_stats)
        return dict_stats

    def save_cost_to_file(self, filename: str):
        """
        Save the cost of the prompt, completion, and the total cost to a file.
        """
        file_op.save_dict_to_json(self.get_stats(), filename)


# for export
claude_client = AnthropicClient()


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
    ret = AnthropicClient().chat_single_turn('what is your version?',
                                             model=models.MDL_CLAUDE_3_OPUS)
    print(ret)


if __name__ == "__main__":
    main()
