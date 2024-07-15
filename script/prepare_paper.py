import os
import sys
import argparse

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')

from lib import helper
from converter.pdf2zip import pdf_text_tabel_to_zip
from extractor.extract_main import save_txt_from_zip


def main():
    """
    A command line interface for the PDF2ZIP extractor.
    parameters
    None
    :return:
    None
    """
    desp = 'Prepare a paper. Result is in result/paper-name/paper-name.zip and txt/ folder.'
    parser = argparse.ArgumentParser(description=desp)
    parser.add_argument('-p', '--pdf',
                        type=str,
                        required=True,
                        help="Path of the paper (pdf) to be extracted")


   # Parse arguments
    args = parser.parse_args()

    # validate pdf file exists
    if not os.path.exists(args.pdf):
        raise ValueError(f'{args.pdf} does not exist')
        # it has to be a pdf file
    if not args.pdf.endswith(".pdf"):
        raise ValueError(f'{args.pdf} is not PDF file.')

    # set save folder
    paper_name = helper.get_file_name_no_ext(args.pdf)
    save_extract_pdf_folder = f"{this_file_path}/../result/{paper_name}"
    os.makedirs(save_extract_pdf_folder, exist_ok=True)
    zip_abs_path=f"{save_extract_pdf_folder}/{paper_name}.zip"
    pdf_text_tabel_to_zip(args.pdf, save_zip_path=zip_abs_path)

    txt_folder = save_extract_pdf_folder
    if save_txt_from_zip(zip_abs_path, txt_folder) is False:
        print(f"Failed to extract {args.pdf} to {txt_folder}")
        return False

    return

if __name__ == "__main__":
    main()
