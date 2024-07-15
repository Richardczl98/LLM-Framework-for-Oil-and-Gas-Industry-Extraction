import os
import sys
import json
import os.path
import zipfile
from collections import OrderedDict
from glob import glob
from tqdm import tqdm

this_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_file_path + '/../')

from converter.excel2txt import excel2txt, excel_to_csv_to_text


def zip_to_text(zip_file, mode='csv'):
    """
    convert zip file to text.
    :param zip_file:
    :return: str
    """
    whole_paper = ""
    archive = zipfile.ZipFile(zip_file, 'r')
    extract_folder = zip_file.replace(".zip", "")
    if not os.path.exists(extract_folder):
        os.mkdir(extract_folder)
    archive.extractall(path=extract_folder)
    with open(extract_folder + "/structuredData.json", "r") as f:
        data = json.load(f)
        for element in data["elements"]:
            if "Text" in list(element.keys()):
                text = element['Text']
                # Table remove and special char remove -   no header and footer
                if "Table" not in element["Path"] and "Lbl" not in element["Path"]:
                    whole_paper = whole_paper + text + "\n"
            if "filePaths" in list(element.keys()):
                text = element['filePaths']
                path_table = extract_folder + "/" + text[0]
                if mode == 'csv':
                    tabel_text = excel_to_csv_to_text(path_table)
                else:
                    tabel_text = excel2txt(path_table)
                whole_paper = whole_paper + tabel_text
    return whole_paper

# if save_to_disk is True, txt files will be saved to 
# zip_file_path/zip_file_name/papers.txt paper-1.txt ...
def zip_to_text_with_page(zip_file, mode="csv", save_to_disk=False,save_folder=None):
    """
    convert zip file to text.
    :param zip_file:
    :return: whole page str and a dict of str page
    """
    archive = zipfile.ZipFile(zip_file, 'r')
    extract_folder = zip_file.replace(".zip", "")
    if not os.path.exists(extract_folder):
        os.mkdir(extract_folder)
    archive.extractall(path=extract_folder)
    with open(extract_folder + "/structuredData.json", "r") as f:
        data = json.load(f)
        pages_list = []
        one_page_text = ""
        init_page = 0
        page_num_list = []
        for index, element in enumerate(data["elements"]):
            if "Text" in list(element.keys()):
                text = element['Text']
                # Table remove and special char remove -   no header and footer
                if "Table" not in element["Path"] and "Lbl" not in element["Path"]:
                    if element["Page"] == init_page:
                        one_page_text += text + "\n"
                        if index == len(data["elements"]) - 1:
                            pages_list.append(one_page_text)
                            page_num_list.append(init_page)
                    else:
                        # the last page
                        if index == len(data["elements"]) - 1:
                            pages_list.append(one_page_text)
                            page_num_list.append(init_page)
                            pages_list.append(text)
                            page_num = element["Page"]
                            page_num_list.append(page_num)
                        else:
                            # Not the last page
                            if one_page_text != "":
                                page_num_list.append(init_page)
                                pages_list.append(one_page_text)
                            init_page = element["Page"]
                            one_page_text = ""
                            one_page_text += text + "\n"
                elif "Table" in element["Path"] and "Lbl" not in element["Path"]:
                    if index != len(data["elements"]) - 1:
                        if element["Path"].startswith(tabel_name) and not data["elements"][index + 1][
                            "Path"].startswith(tabel_name):
                            tabel_end_page = element["Page"]
                            if tabel_end_page != tabel_start_page:
                                page_s2e = "%d-%d" % (tabel_start_page, tabel_end_page)
                                page_num_list.append(page_s2e)
                                pages_list.append(one_page_text)
                                init_page = tabel_end_page
                                one_page_text = ''
            if "filePaths" in list(element.keys()):  # A table may span multiple pages #TODU page
                text = element['filePaths']
                path_table = extract_folder + "/" + text[0]
                if mode == "csv":
                    tabel_text = excel_to_csv_to_text(path_table)
                else:
                    tabel_text = excel2txt(path_table)
                tabel_start_page = element["Page"]
                if element["Page"] == init_page:
                    one_page_text += tabel_text + "\n"
                else:
                    if one_page_text != "":
                        page_num_list.append(init_page)
                        pages_list.append(one_page_text)
                    init_page = element["Page"]
                    one_page_text = ""
                    one_page_text += tabel_text + "\n"
                tabel_name = element["Path"]

    page_dict = OrderedDict()
    whole_text_with_page = ""
    for index, key in enumerate(page_num_list):
        if isinstance(key, int):
            page_dict[key + 1] = pages_list[index]
            whole_text_with_page += f"This is the beginning of page {key + 1}\n"
            whole_text_with_page += pages_list[index]
            whole_text_with_page += f"This is the end of page {key + 1}<\n"

        else:
            s, e = key.split("-")
            s = int(s)
            e = int(e)
            if index != len(page_num_list) - 1 and e == page_num_list[-1]:
                pages_list[index] += pages_list[index + 1]
                page_num_list.remove(page_num_list[index + 1])
                del pages_list[index + 1]
            page_dict["%d-%d" % (s + 1, e + 1)] = pages_list[index]
            whole_text_with_page += f"This is the beginning of page {s + 1}-{e + 1}\n"
            whole_text_with_page += pages_list[index]
            whole_text_with_page += f"This is the end of page {s + 1}-{e + 1}<\n"

    if save_to_disk:
        if save_folder:
            extract_folder = save_folder
        with open(f"{extract_folder}/paper.txt", "w") as f:
            f.write(whole_text_with_page)
        for key, val in page_dict.items():
            save_txt_name = f"paper-{key}.txt"
            with open(f"{extract_folder}/{save_txt_name}", "w") as f:
                f.write(val)
    return whole_text_with_page

def zip_to_text_by_page(zip_file, mode="csv", save_to_disk=False):
    """
    convert zip file to text.
    :param zip_file:
    :return: whole page str and a dict of str page
    """
    whole_paper = ""
    archive = zipfile.ZipFile(zip_file, 'r')
    extract_folder = zip_file.replace(".zip", "")
    if not os.path.exists(extract_folder):
        os.mkdir(extract_folder)
    archive.extractall(path=extract_folder)
    with open(extract_folder + "/structuredData.json", "r") as f:
        data = json.load(f)
        pages_list = []
        one_page_text = ""
        init_page = 0
        page_num_list = []
        tabel_flag = False
        for index, element in enumerate(data["elements"]):
            if "Text" in list(element.keys()):
                text = element['Text']
                # Table remove and special char remove -   no header and footer
                if "Table" not in element["Path"] and "Lbl" not in element["Path"]:
                    whole_paper = whole_paper + text + "\n"
                    if element["Page"] == init_page:
                        one_page_text += text + "\n"
                        if index == len(data["elements"]) - 1:
                            pages_list.append(one_page_text)
                            page_num_list.append(init_page)
                    else:
                        # the last page
                        if index == len(data["elements"]) - 1:
                            pages_list.append(one_page_text)
                            page_num_list.append(init_page)
                            pages_list.append(text)
                            page_num = element["Page"]
                            page_num_list.append(page_num)
                        else:
                            # Not the last page
                            if one_page_text != "":
                                page_num_list.append(init_page)
                                pages_list.append(one_page_text)
                            init_page = element["Page"]
                            one_page_text = ""
                            one_page_text += text + "\n"
                elif "Table" in element["Path"] and "Lbl" not in element["Path"]:
                    if index != len(data["elements"]) - 1:
                        if element["Path"].startswith(tabel_name) and not data["elements"][index + 1][
                            "Path"].startswith(tabel_name):
                            tabel_end_page = element["Page"]
                            if tabel_end_page != tabel_start_page:
                                page_s2e = "%d-%d" % (tabel_start_page, tabel_end_page)
                                page_num_list.append(page_s2e)
                                pages_list.append(one_page_text)
                                init_page = tabel_end_page
                                one_page_text = ''
            if "filePaths" in list(element.keys()):  # A table may span multiple pages #TODU page
                text = element['filePaths']
                path_table = extract_folder + "/" + text[0]
                if mode == "csv":
                    tabel_text = excel_to_csv_to_text(path_table)
                else:
                    tabel_text = excel2txt(path_table)
                tabel_start_page = element["Page"]
                if element["Page"] == init_page:
                    one_page_text += tabel_text + "\n"
                else:
                    if one_page_text != "":
                        page_num_list.append(init_page)
                        pages_list.append(one_page_text)
                    init_page = element["Page"]
                    one_page_text = ""
                    one_page_text += tabel_text + "\n"
                whole_paper = whole_paper + tabel_text
                tabel_name = element["Path"]

    page_dict = OrderedDict()
    for index, key in enumerate(page_num_list):
        if isinstance(key, int):
            page_dict[key + 1] = pages_list[index]
        else:
            s, e = key.split("-")
            s = int(s)
            e = int(e)
            if index != len(page_num_list) - 1 and e == page_num_list[-1]:
                pages_list[index] += pages_list[index + 1]
                page_num_list.remove(page_num_list[index + 1])
                del pages_list[index + 1]
            page_dict["%d-%d" % (s + 1, e + 1)] = pages_list[index]

    if save_to_disk:
        with open(f"{extract_folder}/paper.txt", "w") as f:
            f.write(whole_paper)
        for key, val in page_dict.items():
            save_txt_name = f"paper-{key}.txt"
            with open(f"{extract_folder}/{save_txt_name}", "w") as f:
                f.write(val)
    return whole_paper, page_dict


def zip_to_text_by_page_without_reference(zip_file, mode="csv", save_to_disk=False):
    """
    convert zip file to text.
    :param zip_file:
    :return: whole page str and a dict of str page
    """
    whole_paper = ""
    archive = zipfile.ZipFile(zip_file, 'r')
    extract_folder = zip_file.replace(".zip", "")
    if not os.path.exists(extract_folder):
        os.mkdir(extract_folder)
    archive.extractall(path=extract_folder)
    with open(extract_folder + "/structuredData.json", "r") as f:
        data = json.load(f)
        pages_list = []
        one_page_text = ""
        init_page = 0
        page_num_list = []
        flage = True
        for index, element in enumerate(data["elements"]):
            if "Text" in list(element.keys()):
                text = element['Text']
                # Table remove and special char remove -   no header and footer
                if flage:
                    if "Table" not in element["Path"] and "Lbl" not in element["Path"]:
                        if not 'references' == text.strip().lower():  # 避免部分段落时References开头
                            whole_paper = whole_paper + text + "\n"
                            if element["Page"] == init_page:
                                one_page_text += text + "\n"
                                if index == len(data["elements"]) - 1:
                                    pages_list.append(one_page_text)
                                    page_num_list.append(init_page)
                            else:
                                # the last page
                                if index == len(data["elements"]) - 1:
                                    pages_list.append(one_page_text)
                                    page_num_list.append(init_page)
                                    pages_list.append(text)
                                    page_num = element["Page"]
                                    page_num_list.append(page_num)
                                else:
                                    # Not the last page
                                    if one_page_text != "":
                                        page_num_list.append(init_page)
                                        pages_list.append(one_page_text)
                                    init_page = element["Page"]
                                    one_page_text = ""
                                    one_page_text += text + "\n"
                        else:
                            if one_page_text != "":
                                pages_list.append(one_page_text)
                                page_num_list.append(init_page)
                            flage = False
                    elif "Table" in element["Path"] and "Lbl" not in element["Path"]:
                        if index != len(data["elements"]) - 1:
                            if element["Path"].startswith(tabel_name) and not data["elements"][index + 1][
                                "Path"].startswith(tabel_name):
                                tabel_end_page = element["Page"]
                                if tabel_end_page != tabel_start_page:
                                    page_s2e = "%d-%d" % (tabel_start_page, tabel_end_page)
                                    page_num_list.append(page_s2e)
                                    pages_list.append(one_page_text)
                                    init_page = tabel_end_page
                                    one_page_text = ''
                else:
                    text_lower = text.strip().lower()
                    if text_lower.startswith('appendix'):  # 避免部分段落时References开头
                        flage = True
                        whole_paper = whole_paper + text + "\n"
                        if element["Page"] == init_page:
                            one_page_text += text + "\n"
                            if index == len(data["elements"]) - 1:
                                pages_list.append(one_page_text)
                                page_num_list.append(init_page)
                        else:
                            # the last page
                            if index == len(data["elements"]) - 1:
                                pages_list.append(one_page_text)
                                page_num_list.append(init_page)
                                pages_list.append(text)
                                page_num = element["Page"]
                                page_num_list.append(page_num)
                            else:
                                # Not the last page
                                if one_page_text != "":
                                    page_num_list.append(init_page)
                                    pages_list.append(one_page_text)
                                init_page = element["Page"]
                                one_page_text = ""
                                one_page_text += text + "\n"

            if "filePaths" in list(element.keys()):  # A table may span multiple pages #TODU page
                text = element['filePaths']
                path_table = extract_folder + "/" + text[0]
                if mode == "csv":
                    tabel_text = excel_to_csv_to_text(path_table)
                else:
                    tabel_text = excel2txt(path_table)
                tabel_start_page = element["Page"]
                if element["Page"] == init_page:
                    one_page_text += tabel_text + "\n"
                else:
                    if one_page_text != "":
                        page_num_list.append(init_page)
                        pages_list.append(one_page_text)
                    init_page = element["Page"]
                    one_page_text = ""
                    one_page_text += tabel_text + "\n"
                whole_paper = whole_paper + tabel_text
                tabel_name = element["Path"]

    page_dict = OrderedDict()
    for index, key in enumerate(page_num_list):
        if isinstance(key, int):
            page_dict[key + 1] = pages_list[index]
        else:
            s, e = key.split("-")
            s = int(s)
            e = int(e)
            if index != len(page_num_list) - 1 and e == page_num_list[-1]:
                pages_list[index] += pages_list[index + 1]
                page_num_list.remove(page_num_list[index + 1])
                del pages_list[index + 1]
            page_dict["%d-%d" % (s + 1, e + 1)] = pages_list[index]
    if save_to_disk:
        with open(f"{extract_folder}/paper.txt", "w") as f:
            f.write(whole_paper)
        for key, val in page_dict.items():
            save_txt_name = f"paper-{key}.txt"
            with open(f"{extract_folder}/{save_txt_name}", "w") as f:
                f.write(val)
    return whole_paper, page_dict


def zip_to_raw_text_with_page(zip_file):
    """
    convert zip file to text.
    :param zip_file:
    :return:whole page str and a list of str page
    """
    whole_paper = ""
    archive = zipfile.ZipFile(zip_file, 'r')
    extract_folder = zip_file.replace(".zip", "")
    if not os.path.exists(extract_folder):
        os.mkdir(extract_folder)
    archive.extractall(path=extract_folder)
    with open(extract_folder + "/structuredData.json", "r") as f:
        data = json.load(f)
        num_pages = len(data["pages"])
        pages_list = []
        one_page_text = ""
        init_page = 1
        for index, element in enumerate(data["elements"]):
            if "Text" in list(element.keys()):
                text = element['Text']
                whole_paper = whole_paper + text + "\n"
                if element["Page"] + 1 == init_page:
                    one_page_text += text + "\n"
                    save_txt_name = f"paper-{init_page}.txt"
                    if index == len(data["elements"]) - 1:
                        with open(f"../data/spe/{save_txt_name}", "w") as f:
                            f.write(one_page_text)
                else:
                    init_page += 1
                    with open(f"../data/spe/{save_txt_name}", "w") as f:
                        f.write(one_page_text)
                    pages_list.append(one_page_text)
                    one_page_text = ""
                    one_page_text += text + "\n"
    with open("../data/spe/paper.txt", "w") as f:
        f.write(whole_paper)
    return whole_paper, pages_list


def test01():
    whole_paper1 = zip_to_text("spe-115712-ms.zip", 'csv')
    whole_paper2 = zip_to_text("spe-115712-ms.zip", 'xlsx')
    print(whole_paper1)
    print(whole_paper2)


def test_unzip(doc_num: str):
    file_name = f'../data/zips/spe-{doc_num}-ms.zip'
    whole_paper = zip_to_text_with_page(file_name, 
                                        save_to_disk = True)
    print(whole_paper)

def test03():
    whole_paper, pages_list = zip_to_text_by_page(
        "/Users/57block/Desktop/pdf2excel/PaperDataset/Others/arma-2017-0552.zip")
    print(whole_paper)
    # print(pages_list)


def test04():
    folder = '/Users/57block/Desktop/pdf2excel/PaperDataset/'
    zip_list = glob(os.path.join(folder, "*/*.zip"))
    print(len(zip_list))
    for zip_file in tqdm(zip_list):
        try:
            whole_paper, pages_dict = zip_to_text_by_page(zip_file)
            # print(whole_paper)
            # print(pages_dict.keys())
            for key in pages_dict.keys():
                if isinstance(key, str):
                    print(zip_file)
                    pass
        except:
            print("error")


if __name__ == '__main__':
    # zip2text("../spe-115712-ms.zip")
    test_unzip('115712')
