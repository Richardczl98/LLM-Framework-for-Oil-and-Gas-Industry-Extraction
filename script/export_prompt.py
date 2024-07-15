import os
import sys
import argparse

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')
from model import prompt_template as pt
from model import models
from lib import file_op

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
    A command line interface for export prompt
    parameters
    None
    :return:
    None
    """
    desp = 'Export current prompts in opgee for a field.'
    parser = argparse.ArgumentParser(description=desp)
    parser.add_argument('-f', '--field',
                        type=str,
                        required=True,
                        help="Specify an oil field name")

    parser.add_argument('-m', '--model',
                    type = str,
                    choices = ["gpt-4"],
                    default = 'gpt-4',
                    help="gpt-4 only for now. Will support claude-2 later")

    # Parse arguments
    args = parser.parse_args()
    model = args.model
    field = args.field

    folder_suffix = ''
    if models.is_model_openai(model):
        folder_suffix = 'gpt'
    elif models.is_model_anthropic(model):
        folder_suffix = 'claude'
    else:
        return 'model not supported'

    prompt_folder = f'{this_file_path}/sys_prompt/{args.field}-{folder_suffix}'
    os.makedirs(prompt_folder, exist_ok=True)

    if folder_suffix == 'gpt':
        prompt = pt.SYS_MSG_EXTRACTOR
        file_op.write_to_file(prompt, f'{prompt_folder}/sys_msg.txt')

        prompt = pt.pt_sec1_production_method(args.field)
        file_op.write_to_file(prompt, f'{prompt_folder}/production_method.txt')

        prompt = pt.pt_sec2_field_properties(args.field)
        file_op.write_to_file(prompt, f'{prompt_folder}/field_properties.txt')

        prompt = pt.pt_sec3_fluid_properties(args.field)
        file_op.write_to_file(prompt, f'{prompt_folder}/fluid_properties.txt')

        prompt = pt.pt_sec4_production_practices(args.field)
        file_op.write_to_file(prompt, f'{prompt_folder}/production_practices.txt')

        prompt = pt.pt_sec5_processing_practices(args.field)
        file_op.write_to_file(prompt, f'{prompt_folder}/processing_practices.txt')

        prompt = pt.pt_sec6_others(args.field)
        file_op.write_to_file(prompt, f'{prompt_folder}/others.txt')

        print(f'Prompt exported to {prompt_folder}')

    return

if __name__ == "__main__":
    main()
