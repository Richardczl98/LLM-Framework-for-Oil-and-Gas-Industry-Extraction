import asyncio
import json
import sys
import os
import sentencepiece
import math
from pdf2txt.pdf2txt import pdf2txt
def split_text(txt, max_token_size=3500, overlap_size=0):
    sp = sentencepiece.SentencePieceProcessor(model_file='../misc/tokenizer.model')
    prompt_tokens = sp.encode_as_ids(txt)
    txt_token_num = len(prompt_tokens)
    count = math.ceil(txt_token_num / (max_token_size - overlap_size))
    txt_pieces = []
    for i in range(count):
        start = max(i * (max_token_size - overlap_size), 0)
        end = min(start + max_token_size, txt_token_num)
        txt_piece = sp.decode(prompt_tokens[start:end])
        txt_pieces.append(txt_piece)
    return txt_pieces


try:
    import websockets
except ImportError:
    print("Websockets package not found. Make sure it's installed.")

# For local streaming, the websockets are hosted without ssl - ws://
# HOST = 'localhost:5005'
HOST = '38.147.83.14:37649'
URI = f'ws://{HOST}/api/v1/stream'

# For reverse-proxied streaming, the remote will likely host with ssl - wss://
# URI = 'wss://your-uri-here.trycloudflare.com/api/v1/stream'


async def run(context):
    # Note: the selected defaults change from time to time.
    request = {
        'prompt': context
        # we respect ui setting unless we are sure we need to 
        # overwrite it
        # 'prompt': context,
        # 'max_new_tokens': 250,

        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        # 'preset': 'None',
        # 'do_sample': True,
        # 'temperature': 0.7,
        # 'top_p': 0.1,
        # 'typical_p': 1,
        # 'epsilon_cutoff': 0,  # In units of 1e-4
        # 'eta_cutoff': 0,  # In units of 1e-4
        # 'tfs': 1,
        # 'top_a': 0,
        # 'repetition_penalty': 1.18,
        # 'repetition_penalty_range': 0,
        # 'top_k': 40,
        # 'min_length': 0,
        # 'no_repeat_ngram_size': 0,
        # 'num_beams': 1,
        # 'penalty_alpha': 0,
        # 'length_penalty': 1,
        # 'early_stopping': False,
        # 'mirostat_mode': 0,
        # 'mirostat_tau': 5,
        # 'mirostat_eta': 0.1,

        # 'seed': -1,
        # 'add_bos_token': True,
        # 'truncation_length': 2048,
        # 'ban_eos_token': False,
        # 'skip_special_tokens': True,
        # 'stopping_strings': []
    }

    async with websockets.connect(URI, ping_interval=None) as websocket:
        await websocket.send(json.dumps(request))

        yield context  # Remove this if you just want to see the reply

        while True:
            incoming_data = await websocket.recv()
            incoming_data = json.loads(incoming_data)

            match incoming_data['event']:
                case 'text_stream':
                    yield incoming_data['text']
                case 'stream_end':
                    return


async def print_response_stream(prompt):
    async for response in run(prompt):
        print(response, end='')
        sys.stdout.flush()  # If we don't flush, we won't see tokens in realtime.
def split_text(txt, max_token_size=3500, overlap_size=0):
    sp = sentencepiece.SentencePieceProcessor(model_file='../misc/tokenizer.model')
    prompt_tokens = sp.encode_as_ids(txt)
    txt_token_num = len(prompt_tokens)
    count = math.ceil(txt_token_num / (max_token_size - overlap_size))
    txt_pieces = []
    for i in range(count):
        start = max(i * (max_token_size - overlap_size), 0)
        end = min(start + max_token_size, txt_token_num)
        txt_piece = sp.decode(prompt_tokens[start:end])
        txt_pieces.append(txt_piece)
    return txt_pieces

if __name__ == '__main__':
    system_message = "I hope you can help me with the following tasks as a scientist engaged in the field of oil related industries. First I will give you a text taken from the paper, and then you will have to find the answer to the question I asked. When my question is not mentioned in the text or cannot be answered based on this text, you do not answer other content that is not relevant to the question. Your answer should be as concise as possible, and format your answer according to the example of the answer I gave. I'll give you a couple of examples. You need to understand my above requirements with the following examples, and follow the requirements to complete the task."

    example1 = """
           Input：Steam flooding and hot water flooding  were the most effective thermal methods used in former USSR.  Steam flooding was carried out at the following oil fields: Usinskoe, Okha, Katangli, Yzhno-Voznesenskoe, Zybza-Glubokiyi Yar ,Akhtyro-Bugundyrskoe (Russia).
           Question:Which fields are mentioned in the input document？
           Output：[Usinskoe,Okha,Katangli,Yzhno-Voznesenskoe,Zybza-Glubokiyi Yar,Akhtyro-Bugundyrskoe] 
           ================
      """
    example2 = """
            Input：Ozerkinskoe field maximum depth is 1700m.
            Question:What is the maximum depth of the Ozerkinskoe field?
            Output:1700m
       """
    # load data
    text = pdf2txt('/Users/57block/PycharmProjects/OPGEE/opgee/converter/spe-115712-ms.pdf')
    docs = split_text(text, 3500, 500)

    for doc in docs:
        prompt_base = doc
        template = f'''              
            Input:{doc}
            Question:Which fields are mentioned in the input document？If the name of the field ends in a number, possibly a footnote or a reference, remove those numbers.
            Output:           
          '''
        # prompt_query = "Which oil fields are mentioned in the text, if the oil field name ends with a number, please delete the number. Finally, please return the result to me with Spaces spaced by commas. The output does not end with a dot.Do not output anything other than the name of the field."
        prompt_template = f'''[INST] <<SYS>>
           {system_message}
           <</SYS>>
           {template} [/INST]
           '''
    prompt = "In order to make homemade bread, follow these steps:\n1)"
    asyncio.run(print_response_stream(prompt))
