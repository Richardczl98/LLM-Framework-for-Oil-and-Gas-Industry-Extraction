# -*- coding: utf-8 -*-
# Author: Anjing Wang
# Date: Sep-12-2023

"""model related functions"""

MDL_MOCK = 'mock'

MDL_GPT_4 = 'gpt-4'
MDL_GPT_4_32K = 'gpt-4-32k'
MDL_GPT_4_T = 'gpt-4-1106-preview'
MDL_GPT_4_O = 'gpt-4o'
MDL_GPT_35 = 'gpt-3.5-turbo'
MDL_GPT_35_16K = 'gpt-3.5-turbo-16k'
MDL_GPT_35_INSTRUCT = 'gpt-3.5-turbo-instruct'
MDL_GPT_4_EMB_OPENAI = 'text-embedding-ada-002'

MDL_CLAUDE_2 = 'claude-2'
MDL_CLAUDE_2_1 = 'claude-2.1'
MDL_CLAUDE_3_OPUS = 'claude-3-opus-20240229'

MDL_NLPC_LLAMA2 = 'finetuned-llama-2-70b'
MDL_NLPC_CDOLPHIN = 'chatdolphin'

# model code is defined here
# https://ai.google.dev/models/gemini
MDL_GOOG_GEMINI_PRO = 'gemini-1.0-pro'
MDL_GOOG_GEMINI_15 = 'gemini-1.5-pro-latest'

# https://docs.mistral.ai/platform/endpoints/
MDL_MISTRAL_7B = 'open-mistral-7b'  # Mistral-7B-v0.2'
MDL_MISTRAL_8X7B = 'open-mixtral-8x7b' # Mixtral-8X7B-v0.1
MDL_MISTRAL_SMALL = 'mistral-small-latest' # mistral-small-2402 (not opensource)
MDL_MISTRAL_MEDIUM = 'mistral-medium-latest' # internal prototype
MDL_MISTRAL_LARGE = 'mistral-large-latest' # internal prototype

# llama 2 version from hugging face
MDL_HF_LLAMA2_70B = 'Llama-2-70B-chat-GPTQ'

LST_MODEL_SUPPORTED = [
    MDL_GPT_4, MDL_GPT_4_32K, MDL_GPT_4_T, MDL_GPT_4_O,
    MDL_GPT_35, MDL_GPT_35_16K, MDL_GPT_35_INSTRUCT,
    MDL_CLAUDE_2, MDL_CLAUDE_2_1, MDL_CLAUDE_3_OPUS,
    MDL_NLPC_LLAMA2, MDL_NLPC_CDOLPHIN,
    MDL_GOOG_GEMINI_PRO, MDL_GOOG_GEMINI_15,
    MDL_HF_LLAMA2_70B,
    MDL_MISTRAL_7B, MDL_MISTRAL_8X7B,
    MDL_MISTRAL_SMALL, MDL_MISTRAL_MEDIUM, MDL_MISTRAL_LARGE
]


def is_model_openai(model:str) -> bool:
    if is_model_gpt4(model) or \
       is_model_gpt35(model) :
        return True
    else:
        return False


def is_model_gpt4(model:str) -> bool:
    return model.startswith(MDL_GPT_4)


def is_model_gpt35(model:str) -> bool:
    return model.startswith(MDL_GPT_35)


def is_model_nlpcloud(model:str) -> bool:
    ''' check whether a model support nlp cloud '''
    return model in [MDL_NLPC_LLAMA2,
                     MDL_NLPC_CDOLPHIN]


def is_model_google(model:str) -> bool:
    ''' check whether a model belongs to google '''
    return model in [MDL_GOOG_GEMINI_PRO,
                     MDL_GOOG_GEMINI_15]


# only specific version of llama 2 is supported
def is_model_llama2(model:str) -> bool:
    ''' check whether a model is huggingface llama2 '''
    if model in ['Llama-2-70B-chat-GPTQ']:
        return True
    else:
        return False


def is_model_anthropic(model: str) -> bool:
    ''' only specific version of anthropic is supported '''
    return model in [MDL_CLAUDE_2, MDL_CLAUDE_2_1, MDL_CLAUDE_3_OPUS]


def is_model_mistral(model: str) -> bool:
    ''' check whether a model is a supported mistral model '''
    return model in [MDL_MISTRAL_7B, MDL_MISTRAL_8X7B,
                     MDL_MISTRAL_SMALL, MDL_MISTRAL_MEDIUM, MDL_MISTRAL_LARGE]


def is_model_mocked(model: str) -> bool:
    ''' check whether a mocked model is a used '''
    return model in [MDL_MOCK]


def is_model_supported(model:str) -> bool:
    ''' check whether a model is supported '''
    return model in LST_MODEL_SUPPORTED


if __name__ == '__main__':
    print(is_model_openai('gpt-3.5-turbo-16k'))

