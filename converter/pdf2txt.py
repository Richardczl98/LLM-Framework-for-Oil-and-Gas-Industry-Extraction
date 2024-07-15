import os
import sys

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')

from converter.pdf2zip import pdf_text_tabel_to_zip
from converter.zip2txt import zip_to_text, zip_to_text_with_page, zip_to_text_by_page_without_reference

def pdf_to_text(pdf_file):
    """
    :param pdf_file:
    :return: str text
    """
    pdf_text_tabel_to_zip(pdf_file)
    text = zip_to_text(pdf_file.replace(".pdf", ".zip"))
    return text

def pdf_to_text_with_page(pdf_file,  mode="csv", save_to_disk=False,save_folder=None):
    """
    :param pdf_file:
    :return: str text and page str list
    """
    pdf_text_tabel_to_zip(pdf_file,save_zip_path=save_folder)
    # text,page_list = zip_to_text_with_page(pdf_file.replace(".pdf",".zip"))
    whole_text_with_page = zip_to_text_with_page(pdf_file.replace(".pdf", ".zip"),mode=mode,save_to_disk=save_to_disk,save_folder=save_folder)
    return whole_text_with_page

# if __name__ == '__main__':
#     pdf_to_text_with_page("/Users/57block/Desktop/pdf2excel/PaperDataset/Gasflooding/spe-202574-ms.pdf")
