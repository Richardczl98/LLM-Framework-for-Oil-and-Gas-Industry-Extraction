# -*- coding: utf-8 -*-
# Author: Anjing Wang
# Date: Aug-02-2023

import os
import sys
import sentencepiece
import tiktoken
from anthropic import Anthropic

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')
from model import models
import model.prompt_template as pt
from lib.my_logger import logger

# give enough overhead for convert sys msg and usr msg to
# the underline format pass to the model
# such as LLama2 instruct format
# for openai chatML format
# https://github.com/openai/openai-python/blob/main/chatml.md
TOKEN_CONVERT_OVERHEAD = 50
# we leave this token space for the LLM output
TOKEN_OUTPUT_FOR_SECTION = 800
TOKEN_OUTPUT_FOR_INDIVIDUAL = 200

OPENAI_4K = 4097
OPENAI_8K = 8192
OPENAI_16K = 16385
OPENAI_32K = 32768
# our rate limit is 80K, so we need to use 80*1000
OPENAI_128K = 80*1000

# return max context window size for different model
def max_token(model:str) -> int:
    if models.is_model_openai(model):
        # https://platform.openai.com/docs/models/gpt-3-5
        if '16k' in model:
            return OPENAI_16K
        elif '32k' in model:
            return OPENAI_32K
        # gpt-3.5-turbo-instruct is also 4K
        elif 'gpt-3.5' in model:
            return OPENAI_4K
        elif '1106-preview' in model or model == models.MDL_GPT_4_O:
            return OPENAI_128K
        elif 'gpt-4' in model:
            return OPENAI_8K
        else:
            return 0
    elif models.is_model_llama2(model):
        # no clear reference for context window size
        # just round to the thousand
        if '32k' in model:
            return 32000
        elif '16k' in model:
            return 16000
        elif '8k' in model:
            return 8000
        else:
            return 4000
    elif model == models.MDL_CLAUDE_2:
        return 100*1000
    elif models.is_model_anthropic(model):
        # claude 3 has 200K context window
        return 200*1000
    # https://docs.nlpcloud.com/#chatbot-and-conversational-ai
    elif model == models.MDL_NLPC_LLAMA2:
        return 4000
    elif model == models.MDL_NLPC_CDOLPHIN:
        return 16000
        # need to change 9k for some paper when tbl is too long
        # do not need to spend time debugging as chatdolphine
        # is not important
        # return 9000
    elif model == models.MDL_GOOG_GEMINI_PRO:
          # since we estimate the token, we minus 2000
        return 32000 - 2000
    elif model == models.MDL_GOOG_GEMINI_15:
        # since we estimate the token, we minus 20000
        return 128000 - 2000
    elif model == models.MDL_MISTRAL_7B:
        # only 7b is 8K windows, and rest is 32k
        # since we estimate the token, we minus 400
        return 8000-400
    elif models.is_model_mistral(model):
        # since we estimate the token, we minus 2000
        return 32000 - 2000
    else:
        return 0


def max_token_usr_msg(model: str, sys_msg: str = pt.SYS_MSG_EXTRACTOR) -> int:
    '''
      [sys-msg + usr-msg = (ref + question)]
      [] is the overhead to convert to text model can consume
      return: the max token of sum(ref, question) can be
    '''
    token_max = max_token(model)
    token_sys = count_tokens(model, sys_msg)
    token_concat = count_tokens(model,
                                pt.pt_concatenate_question_ref('',''))

    if models.is_model_gpt35(model):
        token_reserved_for_output = TOKEN_OUTPUT_FOR_INDIVIDUAL
    else:
        token_reserved_for_output = TOKEN_OUTPUT_FOR_SECTION

    return token_max - token_sys - token_concat \
           - TOKEN_CONVERT_OVERHEAD - token_reserved_for_output

def get_spp(model:str):
    model_tokenizer_file = this_file_path + '/' + model + '/tokenizer.model'
    spp = sentencepiece.SentencePieceProcessor(model_file=model_tokenizer_file)
    return spp

# 'Llama-2-70B-chat-GPTQ'
# and all Chatgpt 3.5 or 4 models
# gpt-4, gpt-3.5-turbo-16k etc.
def get_tokens(model:str, prompt:str) -> list:
    if models.is_model_openai(model):
        # use tiktoken to estimate tokens for google gemini
        encoding = tiktoken.encoding_for_model(model)
        tokens = encoding.encode(prompt)
        return tokens
    elif models.is_model_anthropic(model):
        tokens = Anthropic().get_tokenizer().encode(prompt).ids
        return tokens
    elif model == models.MDL_NLPC_CDOLPHIN:
        # use tiktoken to estimate tokens for chat dolphin
        logger.debug('use gpt-4 token to estimate tokens for chat dolphin')
        encoding = tiktoken.encoding_for_model('gpt-4')
        tokens = encoding.encode(prompt)
        return tokens
    elif models.is_model_supported(model):
        # Use Llama-2-70B-chat-GPTQ to estimate tokens
        spp = get_spp('Llama-2-70B-chat-GPTQ')
        tokens = spp.encode_as_ids(prompt)
        return tokens
    else:
        logger.error('Fatal error. Unknown model: %s', model)
        exit(1)

def count_tokens(model:str, prompt:str) -> int:
    return len(get_tokens(model, prompt))

def count_tokens_dir(model:str, dir_path:str):
    dict_rslt = {}
    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                content = file.read()
                num_tokens = count_tokens(model, content)
                dict_rslt[filename] = num_tokens

    for filename, num_tokens in dict_rslt.items():
        print(f'Filename: {filename} num_tokens: {num_tokens}\n')

def token_2_txt(model:str, lst_token:list) -> str:
    if models.is_model_openai(model):
        encoding = tiktoken.encoding_for_model(model)
        return encoding.decode(lst_token)
    elif models.is_model_anthropic(model):
        encoding = Anthropic().get_tokenizer()
        return encoding.decode(lst_token)
    elif model == models.MDL_NLPC_CDOLPHIN:
        # use tiktoken to estimate tokens for chat dolphin
        encoding = tiktoken.encoding_for_model('gpt-4')
        return encoding.decode(lst_token)
    elif models.is_model_nlpcloud(model) or \
         models.is_model_google(model):
        # this is an approximation
        spp = get_spp('Llama-2-70B-chat-GPTQ')
        return spp.decode(lst_token)
    elif models.is_model_supported(model):
        spp = get_spp('Llama-2-70B-chat-GPTQ')
        return spp.decode(lst_token)
    else:
        return ''

def test_count_tokens():
    my_prompt = "Hello World!"
    print(count_tokens('gpt-4', my_prompt))
    return

def test_count_tokens_dir():
    count_tokens_dir('gpt-4', '../data/spe/spe-15712')
    return

if __name__ == '__main__':
    # print(token_2_txt('Llama-2-70B-chat-GPTQ',get_tokens('Llama-2-70B-chat-GPTQ', 'hello world!')))
    # print(max_token_usr_msg('claude-2'))
    # test_count_tokens()
    print(token_2_txt('claude-2', get_tokens('claude-2', 'hello world!')))
