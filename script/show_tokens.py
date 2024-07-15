import os
import sys
import argparse

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')

from lib import helper
from model import tokens
from converter.pdf2zip import pdf_text_tabel_to_zip
from extractor.extract_main import save_txt_from_zip


def verify_paper_prep(paper_name: str) -> str:
    """
    verify that a paper has been prepared
    and return the txt folder of the prepared text
    """
    if '.' in paper_name:
        print('You do not need supply extension.')
        return ''

    if '/' in paper_name:
        print('You do not need supply path.')
        return ''

    result_folder = f'{this_file_path}/../result/{paper_name}'
    zip_abs_path = f'{result_folder}/{paper_name}.zip'
    txt_folder = f'{result_folder}/txt'
    # validate pdf file exists
    if not os.path.exists(zip_abs_path) or \
        not os.path.exists(txt_folder):
        print(f'Use prepare_paper.py to prepare {paper_name} first.')
        return ''
    return txt_folder

def main():
    """
    A command line interface for the PDF2ZIP extractor.
    parameters
    None
    :return:
    None
    """
    desp = 'Show tokens for a paper.'
    parser = argparse.ArgumentParser(description=desp)
    parser.add_argument('-p', '--paper',
                        type=str,
                        required=True,
                        help="The name of the paper. No extension and no path.")

    parser.add_argument('-m', '--model',
                    type = str,
                    choices = ["gpt-4", "claude-2"],
                    default = 'gpt-4',
                    required = False,
                    help="gpt-4 or claude-2. All gpt models have the same token size.")

    # Parse arguments
    args = parser.parse_args()

    txt_folder = verify_paper_prep(args.paper)
    if txt_folder == '':
        return

    lst_files = helper.get_sorted_filenames(txt_folder)

    for txt_file in lst_files:
        txt_file_path = f'{txt_folder}/{txt_file}'
        content = helper.read_file(txt_file_path)
        no_of_tokens = tokens.count_tokens(args.model, content)
        print(f'{txt_file}: {no_of_tokens}')
    return

if __name__ == "__main__":
    main()
