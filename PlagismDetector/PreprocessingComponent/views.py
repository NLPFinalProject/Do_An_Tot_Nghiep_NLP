import math
from string import punctuation
import os, sys
from pptx import Presentation
import pandas as pd
from docx_utils.flatten import opc_to_flat_opc
from xml.dom import minidom
import win32com.client
import uuid
import time
import pythoncom
import csv
from underthesea import sent_tokenize, word_tokenize

sys.path.insert(1, os.getcwd() + "/PreprocessingComponent")
from PreprocessingComponent.pdfminer3 import Pdf_extract

# ------------------------------------các function hỗ trợ cho function DocxToText---------------------------
# Get paragraph string. Input is paragraph element
def ParaString(para):
    string = ""
    # if (str(para)[21:34] not in str(wp_tbl)):# and (str(para)[21:34] not in str(wp_txbx)):
    wt = para.getElementsByTagName("w:t")
    for i in range(len(wt)):
        string = string + wt[i].firstChild.data

    return string


# Get table string. Input is table element
def TableString(table):
    string = ""
    wp = table.getElementsByTagName("w:p")
    column = len(table.getElementsByTagName("w:tc")) / len(
        table.getElementsByTagName("w:tr")
    )
    c = 1
    for i in range(len(wp)):
        string = string + ParaString(wp[i])
        if c % column == 0 and c != len(wp):
            string += ". "
        else:
            string += ". "
        c += 1
    return string


# Get all elements
def getAllElements(lst, type_of_element):
    elements_list = []
    for i in range(len(lst)):
        Elements = lst[i].getElementsByTagName(type_of_element)
        for elm in Elements:
            elements_list.append(elm)
    return elements_list


def ParaToText(p):
    rs = p._element.xpath(".//w:t")
    return u" ".join([r.text for r in rs])


# --------------------------------RÚT TRÍCH TEXT TỪ FILE------------------------------------#
# Docx
def DocxToText(docx_file_name):
    # Parse xml file
    xml_file_name = "mydocx.xml"
    opc_to_flat_opc(docx_file_name, xml_file_name)
    my_docx = minidom.parse(xml_file_name)

    # Get elements
    paragraph = my_docx.getElementsByTagName("w:p")
    table = my_docx.getElementsByTagName("w:tbl")

    # Get all w:p elements in table elements. Output is two-dimensional list
    wp_tbl = getAllElements(table, "w:p")

    # Get text and save to "string" variable
    para_index = 0
    tbl_index = 0
    string = ""
    while para_index < len(paragraph):
        if paragraph[para_index] in wp_tbl:
            string = string + TableString(table[tbl_index])
            para_index += len(table[tbl_index].getElementsByTagName("w:p"))
            tbl_index += 1

        else:
            string = string + ParaString(paragraph[para_index]) + "\n"
            para_index += 1

        string = string + "\n"
    os.remove("mydocx.xml")
    return string


# Doc
def DocToDocx(filename, path=os.getcwd()):
    baseDir = os.path.abspath(os.getcwd())  # Starting directory for directory walk
    pythoncom.CoInitialize()
    word = win32com.client.Dispatch("Word.application")
    file_path = os.path.join(baseDir, filename)
    file_name, file_extension = os.path.splitext(file_path)

    if "~$" not in file_name:
        if file_extension.lower() == ".doc":  #
            # docx_file = '{0}{1}'.format(file_path, 'x')
            docx_file = file_name + str(uuid.uuid4().hex[:10]).format(
                file_path, "x"
            )  # tránh trương hợp có sẵn file .docx tước đó nên thêm phần random để tránh trùng tên
            if not os.path.isfile(
                docx_file
            ):  # Skip conversion where docx file already exists

                file_path = os.path.abspath(file_path)
                docx_file = os.path.abspath(docx_file)

                try:
                    wordDoc = word.Documents.Open(file_path)
                    wordDoc.SaveAs2(docx_file, FileFormat=16)
                    wordDoc.Close()
                except Exception as e:
                    print("Failed to Convert: {0}".format(file_path))
                    print(e)
            return docx_file + ".docx"  ## trả ra tên file đã chuyển từ doc -> docx


# Powerpoint
def PptToText(filename):
    ppt = Presentation(filename)
    string = ""
    for slide in ppt.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                string += shape.text + "\n"
    return string


# CSV
def CsvToText(filename):
    string = ""
    with open(filename, "rt", encoding="utf-8") as f:
        data = csv.reader(f)
        for row in data:
            for cell in row:
                if cell != "":
                    string += cell + "\n"
    return string


# Excel
# hàm rút trich các câu từ file excel ### cần cập nhật thêm vì chưa hoàn thiện
def XlsxToText(filename):
    file_name, file_extension = os.path.splitext(filename)
    data = pd.read_excel(filename, index_col=0, keep_default_na=0)
    filename_csv = file_name + str(uuid.uuid4().hex[:10]) + ".csv"
    data.to_csv(filename_csv, encoding="utf-8")
    res = CsvToText(filename_csv)
    os.remove(filename_csv)
    return res


# --------------------------------TÁCH ĐOẠN, TÁCH CÂU, TÁCH TỪ------------------------------------#

# Tách đoạn
def ListPara(document):
    return document.split("\n")


# Tách câu
def ParaToSentence(para):
    return sent_tokenize(para)


def ListSentence(para_list):
    sentences = []

    for p in para_list:
        sentences.extend(ParaToSentence(p))

    return sentences


# Tách từ
# Giữa các chữ trong 1 từ CÓ dấu gạch dưới (underscore)
def SentenceTowordUnderscore(sentence):
    words = word_tokenize(sentence)

    for i in range(len(words)):
        words[i] = words[i].replace(" ", "_")

    return words


# Giữa các chữ trong 1 từ KHÔNG CÓ dấu gạch dưới (underscore)
def SentenceToWord(sentence):
    return word_tokenize(sentence)


def ListWord(para_list):
    sentences = ListSentence(para_list)

    words = []
    for s in sentences:
        words.append(SentenceToWord(s))

    return words


# Số từ của mỗi câu trong văn bản
def NumOfWord(words_list):
    lst = []

    for sent in words_list:
        lst.append(len(sent))

    return lst


# Ghép các từ thành 1 câu
# Input: word_list [word1, word2, word3,...]
# Output: string
def JoinWord(word_list):
    string = ""

    for i in range(len(word_list) - 1):
        string += word_list[i]
        if word_list[i + 1] not in punctuation:
            string += " "
    string += word_list[len(word_list) - 1]

    return string


# Chia nhỏ câu nếu câu có độ dài > max_len (nhập thủ công)
# Input:
#   + sentence (string)
#   + max_len: độ dài tối đa của 1 câu
# Output: list các sentence mới (string)
def SplitSent(sentence, max_len):
    lst = []

    words = SentenceTowordUnderscore(sentence)
    new_sen = JoinWord(words)

    x = math.ceil(len(new_sen) / max_len)
    new_len = math.ceil(len(new_sen) / x)

    start = 0
    end = new_len
    for i in range(x - 1):
        string = new_sen[start:end]

        index = end - 1
        if new_sen[index] != " ":
            for j in range(index + 1, len(new_sen)):
                if new_sen[j] == " ":
                    break
                string += new_sen[j]
            start = j + 1
            end = start + new_len

        else:
            start += new_len
            end = start + new_len

        lst.append(string.strip().replace("_", " "))
        string = ""

    lst.append(new_sen[start:].strip().replace("_", " "))

    return lst


# Input: list sentences
# Output: list các sentence mới thỏa điều kiện chia nhỏ và sentence cũ
def SplitSentList(sent_list, max_len):
    new_lst = []
    min_len = 5  # cas cau co it hon 5 tu
    for sent in sent_list:
        if len(sent) > max_len:
            new_lst.extend(SplitSent(sent, max_len))
        elif len(sent) > min_len:
            new_lst.append(sent)

    return new_lst


# --------------------------------TIỀN XỬ LÝ------------------------------------#


def preprocess(filename):
    name, file_extension = os.path.splitext(filename)
    para = []

    extension = [".doc", ".docx", ".pdf", ".xlsx", ".csv", ".pptx", ".txt"]

    if file_extension.lower() not in extension:
        raise TypeError("Wrong type document file!")

    else:
        if file_extension.lower() == ".doc":
            new_filename_docx = DocToDocx(filename)
            doc = DocxToText(new_filename_docx)

        if file_extension.lower() == ".docx":
            doc = DocxToText(filename)

        if file_extension.lower() == ".pdf":
            para = Pdf_extract.pdfToText(filename)

        if file_extension.lower() == ".xlsx":
            doc = XlsxToText(filename)

        if file_extension.lower() == ".csv":
            doc = CsvToText(filename)

        if file_extension.lower() == ".pptx":
            doc = PptToText(filename)

        if file_extension.lower() == ".txt":
            f = open(filename, "r", encoding="utf-8")
            doc = f.read()
            f.close()

    if file_extension.lower() != ".pdf":
        para = ListPara(doc)

    list_sent_1 = SplitSentList(ListSentence(para), 450)
    list_sent = [sen.replace("\xa0", "") for sen in list_sent_1]
    ListWords = ListWord(para)

    return list_sent, ListWords, os.path.basename(filename)


if __name__ == "__main__":
    FILE_PATH = "project_doc.docx"

    start_time = time.time()

    sent, word, filename = preprocess(FILE_PATH)
    print("ds câu: ", sent, "\n\n\n word: ", word, "\n\n\nfilename", filename)
    end_time = time.time()

    print("Time:", end_time - start_time)
