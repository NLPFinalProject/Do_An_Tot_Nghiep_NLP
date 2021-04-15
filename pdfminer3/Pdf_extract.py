from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io
from vncorenlp import VnCoreNLP


# Hàm xử lý, chia văn bản thành các đoạn
# Input:
#   + text: kiểu string, văn bản cần chia
# Output:
#   + list_para: list các đoạn

def split_text(text):
    text = text.replace('..', '\n')
    list_para = text.split("\n\n")
    for i in range(len(list_para)):
        list_para[i] = list_para[i].replace('\n', '')
    i = 0
    MAX_DEL_ELE = 8
    len_list = len(list_para)
    while(i < len_list):
        if(len(list_para[i]) < MAX_DEL_ELE):
            del list_para[i]
            i -= 1
            len_list -= 1
        i += 1
    list_para = list(filter(str.strip, list_para))
    return list_para

# Hàm đọc file pdf trả ra list các text theo các trang có áp dụng chia đoạn
# Input:
#   + file_path: Vị trị lưu file pdf cần đọc
# Output:
#   + list_para: list các văn bản đọc theo trang, 1 trang là list các đoạn văn bản của trang đó
# Ví dụ:
#   list_para[3][2]: Trang thứ 4, đoạn thứ 3

def pdf2txt_page(file_path):
    list_page = []
    with open(file_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
            list_page.append(fake_file_handle.getvalue())
            converter.close()
            fake_file_handle.close()
    list_para = []
    for i in range(len(list_page)):
        list_para.append(split_text(list_page[i]))

    return list_para

# Hàm đọc file pdf trả ra text và chia thành list đoạn cho text đó
# Input:
#   + file_path: Vị trị lưu file pdf cần đọc
#   + pages: nếu để trống thì đọc từ đầu đến cuối file
#           nếu có tham số là iteration thì đọc từ page a đến page b
# Output:
#   + list_para: list các đoạn của văn bản
# Ví dụ:
#   pdf2txt("sample.pdf"): Đọc toàn bộ văn bản
#   pdf2txt("sample.pdf", pages = range(1,6)): Đọc văn bản từ trang 2 đến trang 6
#   list_para[0]: Đoạn thứ 1 của văn bản
def pdf2txt(file_path, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = io.StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(file_path, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    print(text)
    output.close
    list_para = split_text(text)

    return list_para

# Đọc theo số trang
# Input:
#    + start_page: trang đầu tiên
#    + end_page: trang cuối cùng
#    + doc_file: file .pdf cần đọc
# Output:
#    + Tương tự output của vncorenlp.tokenize
# Ví dụ:
# Đọc từ trang 4 tới trang 7: read_pages(4, 7)
# Đọc duy nhất trang 5: read_pages(5, 5)
def read_pages(start_page, end_page, doc_file):
    VNCORENLP_FILE_PATH = 'VnCoreNLP/VnCoreNLP-1.1.1.jar'
    vncorenlp = VnCoreNLP(VNCORENLP_FILE_PATH)

    words = []
    doc = pdf2txt(doc_file, range(start_page - 1, end_page))
    for para in doc:
        words.extend(vncorenlp.tokenize(para))

    return words
