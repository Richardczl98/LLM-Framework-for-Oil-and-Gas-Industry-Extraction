# -*- coding: utf-8 -*-
# Author: Anjing Wang
# Date: Jan-15-2024
"""
Extract all pdfs in a directory
"""

import os
import sys
import argparse
import subprocess

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')

from lib import helper
from converter.pdf2zip import pdf_text_tabel_to_zip
from extractor.extract_main import save_txt_from_zip


def main():
    """
    A command line interface for extracting all pdfs in a directory
    """
    desp = 'Extract all pdfs in a directory'
    parser = argparse.ArgumentParser(description=desp)
    parser.add_argument('-d', '--dir',
                        type = str,
                        required = True,
                        help = 'Directory that contains all pdf to be extracted')

    # Parse arguments
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        print(f"Directory {args.dir} does not exist.")
        return

    files = os.listdir(args.dir)
    pdf_files = []
    for file in files:
        if file.lower().endswith('.pdf'):
            pdf_files.append(file)

    if len(pdf_files) == 0:
        print('No pdf files found in the directory.')
        return

    for pdf_file in pdf_files:
        # try to find zip file
        zip_file = pdf_file.replace('.pdf', '.zip')
        zip_file_path = os.path.join(this_file_path + '/../data/zips/', zip_file)
        if os.path.exists(zip_file_path):
            print(f'zip file {zip_file} found, skip')
        else:
            pdf_file_path = os.path.join(args.dir, pdf_file)
            pdf_text_tabel_to_zip(pdf_file_path, save_zip_path=zip_file_path)
            print('zip file created: ' + zip_file)

        print(f'Start to extract {pdf_file}')
        cmd = ['python', 'opgee_cli.py',
                '-p', zip_file_path,
                '-s', 'individual',
                '-m', 'gpt-4',
                '-d']
        subprocess.run(cmd,
                       cwd = this_file_path + '/../',
                       capture_output = True,
                       text = True,
                       check =  False)
    return

if __name__ == "__main__":
    main()

