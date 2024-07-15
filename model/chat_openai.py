# -*- coding: utf-8 -*-
# Author: Anjing Wang
# Date:   Jun-29-2023

import os
import sys

import numpy as np
from openai import AzureOpenAI, OpenAI
# do not need organization id for api to work properly
# openai.organization = 'org-xxx'
from decouple import config
import traceback
from typing import Optional

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')
from model import models, tokens
from lib.my_logger import logger
from lib import opgee_def
from lib import file_op
import model.prompt_template as pt
from lib.my_logger import logger


# mem_round is only for testing purpose the key
# when extract, we do not need multiple rounds
MEM_ROUNDS = 20
# in file config, make it more searchable
GPT_TEMPERATURE = 0.6


class OpenAIClient:
    def __init__(self):
        # a list to keep user messages
        self._msg_usr = []
        # a list to keep AI generated messages
        # _msg_usr[0], _msg_assistant[0],
        # _msg_usr[1], _msg_assistant[1],
        # _msg_usr[2], _msg_assistant[2]
        # this is the conversation history
        self._msg_assistant = []

        # dn is deployment name
        self._dn = ''
        self._current_model = ''
        self._is_use_azure = False

        self._client_azure_embedding = None
        self._client_azure_gpt35 = None
        self._client_azure_gpt4 = None
        self._client_azure_gpt4o = None
        self._client_openai = None
        self._init_clients()

        # counters go up from 0
        # https://platform.openai.com/docs/models/gpt-4
        self._no_of_tokens_completion = {
            models.MDL_GPT_4: 0,  # 8k
            models.MDL_GPT_4_32K: 0, # 32k
            models.MDL_GPT_35: 0, # 4k
            models.MDL_GPT_35_16K: 0, # 16k
            models.MDL_GPT_4_T: 0, # 128k
            models.MDL_GPT_4_O: 0 # 128K
        }
        self._no_of_tokens_prompt = {
            models.MDL_GPT_4: 0,  # 8k
            models.MDL_GPT_4_32K: 0, # 32k
            models.MDL_GPT_35: 0, # 4k
            models.MDL_GPT_35_16K: 0,# 16k
            models.MDL_GPT_4_T: 0, # 128k
            models.MDL_GPT_4_O: 0
        }

    @property
    def is_use_azure(self):
        """ Getter for _is_use_azure """
        return self._is_use_azure

    def _init_clients(self):
        self._is_use_azure = config('AZURE_OPENAI', default=False, cast=bool)
        if self._is_use_azure:
            self._client_azure_embedding = AzureOpenAI(
                api_key=config('AZURE_OPENAI_API_KEY_GPT_EMB'),
                azure_endpoint=config('AZURE_OPENAI_API_BASE_GPT_EMB'),
                azure_deployment=config('AZURE_OPENAI_DN_EMB'),
                api_version=config('AZURE_OPENAI_API_VERSION')
            )
            self._client_azure_gpt35 = AzureOpenAI(
                api_key=config('AZURE_OPENAI_API_KEY_GPT_35'),
                azure_endpoint=config('AZURE_OPENAI_API_BASE_GPT_35'),
                api_version=config('AZURE_OPENAI_API_VERSION')
            )
            self._client_azure_gpt4 = AzureOpenAI(
                api_key=config('AZURE_OPENAI_API_KEY_GPT_4'),
                azure_endpoint=config('AZURE_OPENAI_API_BASE_GPT_4'),
                api_version=config('AZURE_OPENAI_API_VERSION')
            )
            self._client_azure_gpt4o = AzureOpenAI(
                api_key=config('AZURE_OPENAI_API_KEY_GPT_4_O'),
                azure_endpoint=config('AZURE_OPENAI_API_BASE_GPT_4_O'),
                api_version=config('AZURE_OPENAI_API_VERSION')
            )
            self._client_openai = None
        else:
            self._client_azure_embedding = None
            self._client_chatgpt = None
            self._client_azure_gpt4 = None
            self._client_azure_gpt4o = None
            self._client_openai = OpenAI(
                api_key=config('OPENAI_API_KEY')
            )

    # keep last _MEM_ROUNDS of messages in the list
    # this is a FIFO queue,  1st-2nd-3rd message
    def _add_message(self, messages, new_message):
        if len(messages) < MEM_ROUNDS:
            messages.append(new_message)
        else:
            messages.pop(0)
            messages.append(new_message)
        return messages

    def _openai_api_embedding(self, msgs):
        try:
            if self._is_use_azure:
                response = self._client_azure_embedding.embedding.create(
                    input=msgs,
                    model=config('AZURE_OPENAI_DN_EMB')
                )
            else:
                response = self._client_openai.embedding.create(
                    input=msgs,
                    model=models.MDL_GPT_4_EMB_OPENAI,
                )
        except Exception as err:
            logger.error(err)
            return []
        return response['data'][0]['embedding']

    def _openai_api_chat(self, msgs, model: str, response_format: Optional[dict] = None):
        response = None
        if self._is_use_azure:
            if models.is_model_gpt4(model):
                if model == models.MDL_GPT_4_O:
                    engine = config('AZURE_OPENAI_DN_GPT_4_O')
                    response = self._client_azure_gpt4o.chat.completions.create(
                        model=engine,
                        messages=msgs,
                        temperature=GPT_TEMPERATURE,
                        response_format=response_format
                    )
                else:
                    if model == models.MDL_GPT_4:
                        engine = config('AZURE_OPENAI_DN_GPT_4')
                    elif model == models.MDL_GPT_4_32K:
                        engine = config('AZURE_OPENAI_DN_GPT_4_32K')
                    elif model == models.MDL_GPT_4_T:
                        engine = config('AZURE_OPENAI_DN_GPT_4_T')

                    response = self._client_azure_gpt4.chat.completions.create(
                        model=engine,
                        messages=msgs,
                        temperature=GPT_TEMPERATURE,
                        response_format=response_format
                    )
            else:
                engine = config('AZURE_OPENAI_DN_GPT_35_16K')
                response = self._client_azure_gpt35.chat.completions.create(
                    model=engine,
                    messages=msgs,
                    temperature=GPT_TEMPERATURE,
                    response_format=response_format
                )
        else:
            response = self._client_openai.chat.completions.create(
                        model=model,
                        messages=msgs,
                        temperature=GPT_TEMPERATURE,
                        response_format=response_format
                    )

        self._count_tokens(model,
                           response.usage.prompt_tokens,
                           response.usage.completion_tokens)

        logger.debug('openai full response: %s', str(response))

        return response.choices[0].message.content

    # https://platform.openai.com/docs/guides/chat/introduction
    # need to always input history to generate the last response.
    # as the model itself does not remeber the chat history.
    def chat_multi(self,
                   usr_msg: str,
                   model: str = 'gpt-4',
                   sys_msg:str = pt.SYS_MSG_ASSISTANT) -> str:
        """
        Generate a response to a user message in a multi-turn conversation.

        Args:
            usr_msg (str): The user message to respond to.
            model (str, optional): The model to use for generating the response. Defaults to 'gpt-4'.

        Returns:
            str: The generated response.
        """

        msgs = []
        msgs.append({"role": "system",
                    "content": sys_msg})
        # add previous conversation to the msgs
        length = len(self._msg_usr)
        for i in range(length):
            msgs.append({'role': 'user', 'content': self._msg_usr[i]})
            msgs.append({'role': 'assistant', 'content': self._msg_assistant[i]})

        msgs.append({'role': 'user', 'content': usr_msg})

        resp = self._openai_api_chat(msgs, model)

        # add this round conversation back to the queue
        _msg_usr = self._add_message(self._msg_usr, usr_msg)
        _msg_assistant = self._add_message(self._msg_assistant, resp)

        return resp

    def chat_interactive(self,
                         model: str = 'gpt-4o',
                         sys_msg: str = pt.SYS_MSG_ASSISTANT):
        """
        This function provides an interactive chat with the user.

        Parameters:
        None

        Returns:
        None
        """
        while True:
            # Get user input
            prompt = input("Please ask me anything or type 'exit' to quit: ")

            # Check if the user entered 'exit'
            if prompt.lower() == 'exit':
                break

            generated_text = self.chat_multi(prompt,
                                             model,
                                             sys_msg = sys_msg)
            # Print the user input
            print(generated_text + '\n')
            # self.print_token_counters()

    # single-turn chat, no any previous history is provided
    # only support gpt-3.5 and gpt-4
    def chat_single_turn(self,
                         usr_msg: str,
                         model: str = 'gpt-4o',
                         sys_msg: str = pt.SYS_MSG_EXTRACTOR,
                         json_format: bool = False) -> str:
        """
        Performs a single turn of a chat conversation using the specified model.

        Args:
            usr_msg (str): The user message to be included in the chat conversation.
            model (str, optional): The model to be used for the chat conversation.
                                    Defaults to 'gpt-4o'.
            sys_msg (str): The system message for the chat conversation.
            json_format (bool): The type of the output format. Defaults to False for text, True for json format.

        Returns:
            str: The response generated by the model.
            """
        if json_format:
            response_format = {'type': 'json_object'}
            model = models.MDL_GPT_4_O
        else:
            response_format = None

        msgs = []
        msgs.append({"role": "system",
                    "content": sys_msg})
        msgs.append({'role': 'user',
                    'content': usr_msg})
        try:
            resp = self._openai_api_chat(msgs,
                                         model,
                                         response_format=response_format)
            logger.debug('chatgpt returned text: %s', str(resp))
        except Exception as err:
            logger.exception(err)
            logger.exception(traceback.format_exc())
            raise
        return resp

    def create_embedding(self, usr_msg: str) -> np.array:
        """
        Generate a embedding for user message by using gpt-4 embedding model.

        Args:
            usr_msg (str): The user message to respond to.
        Returns:
            numpy array: A numpy array of float.
        """
        embedding = self._openai_api_embedding(msgs=usr_msg)
        return np.array(embedding)

    def _count_tokens(self, model, prompt_tokens, completion_tokens):
        if model == models.MDL_GPT_35:
            self._no_of_tokens_prompt[models.MDL_GPT_35] += prompt_tokens
            self._no_of_tokens_completion[models.MDL_GPT_35] += completion_tokens
        elif model == models.MDL_GPT_4:
            self._no_of_tokens_prompt[models.MDL_GPT_4] += prompt_tokens
            self._no_of_tokens_completion[models.MDL_GPT_4] += completion_tokens
        elif model == models.MDL_GPT_35_16K:
            self._no_of_tokens_prompt[models.MDL_GPT_35_16K] += prompt_tokens
            self._no_of_tokens_completion[models.MDL_GPT_35_16K] += completion_tokens
        elif model == models.MDL_GPT_4_32K:
            self._no_of_tokens_prompt[models.MDL_GPT_4_32K] += prompt_tokens
            self._no_of_tokens_completion[models.MDL_GPT_4_32K] += completion_tokens
        elif model == models.MDL_GPT_4_T:
            self._no_of_tokens_prompt[models.MDL_GPT_4_T] += prompt_tokens
            self._no_of_tokens_completion[models.MDL_GPT_4_T] += completion_tokens
        elif model == models.MDL_GPT_4_O:
            self._no_of_tokens_prompt[models.MDL_GPT_4_O] += prompt_tokens
            self._no_of_tokens_completion[models.MDL_GPT_4_O] += completion_tokens

    def get_current_cost(self):
        """
        Get the current cost of the OpenAI API.
        """
        # azure and openai pricing is the same
        # https://azure.microsoft.com/en-gb/pricing/details/cognitive-services/openai-service/
        # https://openai.com/pricing
        cost = self._no_of_tokens_prompt[models.MDL_GPT_4] * 0.03 / 1000 + \
               self._no_of_tokens_completion[models.MDL_GPT_4] * 0.06 / 1000 + \
               self._no_of_tokens_prompt[models.MDL_GPT_4_32K] * 0.06 / 1000 + \
               self._no_of_tokens_completion[models.MDL_GPT_4_32K] * 0.12 / 1000 + \
               self._no_of_tokens_prompt[models.MDL_GPT_35] * 0.0015 / 1000 + \
               self._no_of_tokens_completion[models.MDL_GPT_35] * 0.002 / 1000 + \
               self._no_of_tokens_prompt[models.MDL_GPT_35_16K] * 0.0005 / 1000 + \
               self._no_of_tokens_completion[models.MDL_GPT_35_16K] * 0.0015 / 1000 + \
               self._no_of_tokens_prompt[models.MDL_GPT_4_T] * 0.01 / 1000 + \
               self._no_of_tokens_completion[models.MDL_GPT_4_T] * 0.03 / 1000 + \
               self._no_of_tokens_prompt[models.MDL_GPT_4_O] * 0.005 / 1000 + \
               self._no_of_tokens_completion[models.MDL_GPT_4_O] * 0.015 / 1000
        return cost

    def print_token_counters(self):
        """
        Print the token counters
        """
        print('prompt:' + str(self._no_of_tokens_prompt))
        print('completion' + str(self._no_of_tokens_completion))

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


# for export
openai_client = OpenAIClient()


def main():
    # ret = openai_client.chat_single_turn('hello world! what is your name?',
    #                                      model= models.MDL_GPT_4_32K)
    # print(ret)
    # print(chat_single_turn('hello world! what is your name?'))
    openai_client.chat_interactive(model=models.MDL_GPT_4_O)
    # openai_client._init_clients()
    # print(is_key_support_gpt4())


if __name__ == "__main__":
    main()
    # openai_client.create_embedding(usr_msg='Not_mentioned', model='gpt-4')
