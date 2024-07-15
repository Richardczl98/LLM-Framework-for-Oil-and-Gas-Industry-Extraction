import os
import sys
import json
import requests
import math
from glob import glob
from tqdm import tqdm

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../../converter/')
sys.path.insert(0, this_file_path + '/../../zip2txt/')
sys.path.insert(0, this_file_path + '/../../model/')
sys.path.insert(0, this_file_path + '/../../eval/')
sys.path.insert(0, this_file_path + '/../../lib/')
sys.path.insert(0, this_file_path + '/../../data/')
sys.path.insert(0, this_file_path + '/../../misc/')

HOST = 'localhost:5000'
URI = 'https://xwhpv1zwvvali4-5000.proxy.runpod.net/api/v1/chat'

def chat_multi_turn(user_input, history):
    request = {
        'user_input': user_input,
        'max_new_tokens': 250,
        'history': history,
        'mode': 'instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
        'character': 'Example',
        'instruction_template': 'Vicuna-v1.1',  # Will get autodetected if unset
        # 'context_instruct': '',  # Optional
        'your_name': 'You',
        'regenerate': False,
        '_continue': False,
        'stop_at_newline': False,
        'chat_generation_attempts': 1,
        'chat-instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.7,
        # 'temperature': 0.01,
        'top_p': 0.1,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'repetition_penalty_range': 0,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,

        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    response = requests.post(URI, json=request, stream=True)

    if response.status_code == 200:
        result = response.json()['results'][0]['history']
        print(result['visible'][-1][1])
        return result['visible'][-1][1]
    else:
        print(response)

def chat_single_turn(user_input:str) -> str:
    return 'Hello World'

if __name__ == '__main__':
    print(0)