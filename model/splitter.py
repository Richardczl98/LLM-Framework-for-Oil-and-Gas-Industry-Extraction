import os
import sys
import math
import numpy as np

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')
from model import tokens
from lib.my_logger import logger

# split text to trunks with max token and proper overlap
# the split looks like
# AAAAAAAAAA
#         AABBBBBBBBB
#                  BBCCCCCCC
def split_txt_by_token_size(txt: str,
                            max_token_size: int = 3800,
                            overlap_token_size: int = 100,
                            model: str = 'gpt-4') -> list:
    if len(txt.strip()) == 0:
        logger.error(f'The split text is {txt}.exit!')
        return ''
    prompt_tokens = tokens.get_tokens(model, txt)
    txt_token_num = len(prompt_tokens)

    # Rounding up ensures that the tail data is not lost
    count = math.ceil(txt_token_num / (max_token_size - overlap_token_size))
    if count < 1:
        logger.error('%s / (%s - %s)',
                     txt_token_num,
                     max_token_size,
                     overlap_token_size)
        logger.error('Fatal error. The count of split text is less than 1. exit!')
        exit(1)
    txt_pieces = []
    for i in range(count):
        start = max(i * (max_token_size - overlap_token_size), 0)
        end = min(start + max_token_size, txt_token_num)
        txt_piece = tokens.token_2_txt(model, prompt_tokens[start:end])
        txt_pieces.append(txt_piece)
    return txt_pieces

# When data is stored on a page basis, one or more pages of text need to be
# entered at a time, and the number of tokens may exceed the maximum number
# of tokens in the model.the split looks like
# page_1 page_2
#        page_2 page_3
#               page_3 page4
def split_txt_by_page_num(txt: str,
                          overlap_pages: int = 0,
                          max_token_size: int = 3800,
                          overlap_token_size: int = 100,
                          model: str = 'gpt-4'):
    '''

    :param pages: page list [page_0,page_1,...,page_n]
    :param overlap_pages: Overlapping pages
    :param max_token_size:
    :param overlap_token_size: When multiple pages are entered, the token may exceed the upper limit of the model, and the
     text needs to be shred. A certain number of tokens overlap to enrich contextual semantic information.
    :param model:
    :return: pages list
    '''

    page_txt_list=txt.strip().split("<")[:-1] # remove the last word "

    if len(page_txt_list)==0:
        logger.error(f'The pages list is empty,exit!')
        return ''

    txt_pieces = []
    total_token_size = 0
    merge_token = []
    merge_token_size = []
    for index, page in enumerate(page_txt_list):
        prompt_tokens = tokens.get_tokens(model, page)
        # get token size
        text_token_num = len(prompt_tokens)
        if text_token_num + total_token_size < max_token_size:
            merge_token_size.append(text_token_num)
            total_token_size += text_token_num
            merge_token.append(prompt_tokens)
            # last page
            if index == len(page_txt_list) - 1:
                text_piece = tokens.token_2_txt(model,[i for j in merge_token for i in j])
                txt_pieces.append(text_piece)
        else:
            text_piece = tokens.token_2_txt(model, [i for j in merge_token for i in j])
            # The number of multi-page texts may exceed the token limit
            if np.array(merge_token_size).sum() > max_token_size:
                logger.info("This page token number is %d.It should be split." % (np.array(merge_token_size).sum()))
                text_pieces = split_txt_by_token_size(text_piece, overlap_token_size=overlap_token_size)
                txt_pieces.extend(text_pieces)
            txt_pieces.append(text_piece)
            if overlap_pages > 0:
                # save the overlap pages,token number
                merge_token = merge_token[-1 * overlap_pages:]
                merge_token.append(prompt_tokens)
                merge_token_size = merge_token_size[-1 * overlap_pages:]
                merge_token_size.append(text_token_num)
                total_token_size = np.array(merge_token_size).sum()
            else:
                merge_token = []
                merge_token_size = []
                total_token_size = 0
                total_token_size += text_token_num
                merge_token.append(prompt_tokens)
                merge_token_size.append(text_token_num)
            if index == len(page_txt_list) - 1:
                text_piece = tokens.token_2_txt(model,[i for j in merge_token for i in j])
                if np.array(merge_token_size).sum() > max_token_size:
                    logger.info("This page token number is over %d.It should be split." % (np.array(merge_token_size).sum()))
                    text_pieces = split_txt_by_token_size(text_piece, overlap_token_size=overlap_token_size)
                    txt_pieces.extend(text_pieces)
    return txt_pieces
def split_pages(pages: list,
                overlap_pages: int = 0,
                max_token_size: int = 3800,
                overlap_token_size: int = 100,
                model: str = 'Llama-2-70B-chat-GPTQ'):
    '''

    :param pages: page list [page_0,page_1,...,page_n]
    :param overlap_pages: Overlapping pages
    :param max_token_size:
    :param overlap_token_size: When multiple pages are entered, the token may exceed the upper limit of the model, and the
     text needs to be shred. A certain number of tokens overlap to enrich contextual semantic information.
    :param model:
    :return: pages list
    '''
    if len(pages)==0:
        print(f'The pages list is empty,exit!')
        return ''
    txt_pieces = []
    total_token_size = 0
    merge_token = []
    merge_token_size = []
    for index, page in enumerate(pages):
        prompt_tokens = tokens.get_tokens(model, page)
        # get token size
        text_token_num = len(prompt_tokens)
        if text_token_num + total_token_size < max_token_size:
            merge_token_size.append(text_token_num)
            total_token_size += text_token_num
            merge_token.append(prompt_tokens)
            # last page
            if index == len(pages) - 1:
                text_piece = tokens.token_2_txt(model,[i for j in merge_token for i in j])
                txt_pieces.append(text_piece)
        else:
            text_piece = tokens.token_2_txt(model, [i for j in merge_token for i in j])
            # The number of multi-page texts may exceed the token limit
            if np.array(merge_token_size).sum() > max_token_size:
                print("This page token number is %d.It should be split." % (np.array(merge_token_size).sum()))
                text_pieces = split_txt_by_token_size(text_piece, overlap_token_size=overlap_token_size)
                txt_pieces.extend(text_pieces)
            txt_pieces.append(text_piece)
            if overlap_pages > 0:
                # save the overlap pages,token number
                merge_token = merge_token[-1 * overlap_pages:]
                merge_token.append(prompt_tokens)
                merge_token_size = merge_token_size[-1 * overlap_pages:]
                merge_token_size.append(text_token_num)
                total_token_size = np.array(merge_token_size).sum()
            else:
                merge_token = []
                merge_token_size = []
                total_token_size = 0
                total_token_size += text_token_num
                merge_token.append(prompt_tokens)
                merge_token_size.append(text_token_num)
            if index == len(pages) - 1:
                text_piece = tokens.token_2_txt(model,[i for j in merge_token for i in j])
                if np.array(merge_token_size).sum() > max_token_size:
                    print("This page token number is %d.It should be split." % (np.array(merge_token_size).sum()))
                    text_pieces = split_txt_by_token_size(text_piece, overlap_token_size=overlap_token_size)
                    txt_pieces.extend(text_pieces)
    return txt_pieces


if __name__ == '__main__':
    # print(split_txt_by_token_size('hello world!'))

    with open("/Users/57block/PycharmProjects/OPGEE/opgee/result/spe-115712-ms/231013_1427-gpt-4-test/txt/paper.txt","rb") as f:
        txt=f.readlines()
        print(txt)