from operator import itemgetter
import math
from django.conf import settings
import string

#import preprocessor as p
#import internet as i
from django.conf import settings
from googlesearch import search
import requests
import os
import PreprocessingComponent.views as p
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
from ScrapeSearchEngine.ScrapeSearchEngine import Google
from ScrapeSearchEngine.ScrapeSearchEngine import Duckduckgo
from ScrapeSearchEngine.ScrapeSearchEngine import Givewater
from ScrapeSearchEngine.ScrapeSearchEngine import Bing
from ScrapeSearchEngine.ScrapeSearchEngine import Yahoo
from ScrapeSearchEngine.ScrapeSearchEngine import Ecosia
import urllib.request
userAgent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
             ' Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68')
#search on google "my user agent"

#check a url can be doawnloaded as a file?
def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True
# search keyword from multiple search engine include
#
# def tiny_url(url):
#     apiurl = "http://tinyurl.com/api-create.php?url="
#     tinyurl = urllib.request.urlopen(apiurl + url).read()
#     return tinyurl.decode("utf-8")

import requests
import sys
import traceback
import urllib


# class UrlShortenTinyurl:
#     URL = "http://tinyurl.com/api-create.php"
#
#     def shorten(self, url_long):
#         try:
#             url = self.URL + "?" \
#                 + urllib.parse.urlencode({"url": url_long})
#             res = requests.get(url)
#             # print("STATUS CODE:", res.status_code)
#             # print("   LONG URL:", url_long)
#             # print("  SHORT URL:", res.text)
#         except Exception as e:
#             raise
#         return res.text


def search_keyword(search):
    list_url = []
    res=[]
    list_url.extend(Google(search, userAgent))
    list_url.extend(Bing(search, userAgent))
    list_url.extend( Yahoo(search, userAgent))
    list_url.extend(Duckduckgo(search, userAgent))
    list_url.extend(Givewater(search, userAgent))
    #list_url=list(dict.fromkeys(list_url))
    #obj = UrlShortenTinyurl()

    # for i in range(len(list_url)):
    #     res.append( obj.shorten(list_url[i]))

    # list_url.extend (Ecosia(search, userAgent))
    return list(dict.fromkeys(list_url))

# download file downloadable such as: pdf, docx,...
def download_document(url):
    if (is_downloadable(url)):
        name = os.path.basename(url)
        r = requests.get(url, allow_redirects=True)
        open(settings.MEDIA_ROOT+'/DocumentFile/file_downloaded/' + name, 'wb').write(r.content)
        return settings.MEDIA_ROOT+'/DocumentFile/file_downloaded/' + name

# crawl text from html website then preprocess and give output: list sentence after preprocessing.
def crawl_web(url):
    import platform
    import ssl
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.check_hostname = True
    ssl_context.load_default_certs()

    if platform.system().lower() == 'darwin':
        import certifi
        ssl_context.load_verify_locations(
            cafile=os.path.relpath(certifi.where()),
            capath=None,
            cadata=None)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
             ' Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68'}
    req=Request(url,headers=headers)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, features="html.parser")


    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    temp = p.list_para2txt(text.split("\n"))
    res  = p.convert2listsentence(temp)
    return res #list sentence
# vncorenlp_file = 'D:\DH\TotNghiep\core\preprocessing\VnCoreNLP\VnCoreNLP-1.1.1.jar'
# from vncorenlp import VnCoreNLP
# vncorenlp = VnCoreNLP(vncorenlp_file)

def get_path():
    return os.getcwd()

# Cách chạy chương trình:
# Sửa path của các file và thực thi chương trình 

#DOC_FILE_PATH = 'baocao.docx'
STOPWORD_FILE_PATH = 'stopword.txt'
ALPHABET_FILE_PATH = 'alphabet.txt'


# Thống kê từ loại của một từ. Xem từ đó đóng vai trò bao nhiêu từ loại, mỗi từ loại bao nhiêu lần.
# Input:
#    + word: từ cần thống kê
#    + vncorenlp_postag: postag của vncorenlp
# Output: list các tuple đã sắp xếp giảm dần theo số lượng từ loại
# Ví dụ: [('V', 10), ('N', 6), ('Np', 2)]
def tag_statistic(word, vncorenlp_postag):
    word_tag_dict = {}

    for sen_lst in vncorenlp_postag:
        for w_tpl in sen_lst:
            w = w_tpl[0].lower()
            if word == w:
                if w_tpl[1] in word_tag_dict:
                    word_tag_dict[w_tpl[1]] += 1
                else:
                    word_tag_dict[w_tpl[1]] = 1

    return sorted(word_tag_dict.items(), key = itemgetter(1), reverse = True)


# Tìm vị trí câu chứa một từ nào đó ứng với tag (cho trước) của từ đó trong câu. 
# Ví dụ: Tìm các câu chứa từ 'quân' có tag là 'Np'
# Input:
#    + word: từ cần thống kê
#    + tag: tag ứng với word
#    + vncorenlp_postag: postag của vncorenlp
# Output: list vị trí của các câu thỏa điều kiện (word, tag) trong vncorenlp_postag
def find_sentence_index(word, tag, vncorenlp_postag):
    index = []

    for i in range(len(vncorenlp_postag)):
        for w_tpl in vncorenlp_postag[i]:
            w = w_tpl[0].lower()
            if word == w and w_tpl[1] == tag[0][0]:
                index.append(i)
                break

    return index


# Tách dòng của text và lưu vào mảng
# Input: file .txt
# Output: danh sách các phần tử (list)
def preprocess_text_file(txt_file):
    f = open(txt_file, 'r', encoding='utf-8')
    elements = f.readlines()
    for i in range(len(elements)):
        elements[i] = elements[i].replace('\n', '')
    f.close()

    return elements


# Kiểm tra trong 1 chuỗi có hợp lệ để sử dụng cho thuật toán TF-IDF hay không?
# Ví dụ:
#    + Chuỗi hợp lệ: Nguyễn_Ánh, đồng_minh, lãnh_thổ,...
#    + Chuỗi không hợp lệ: 1972, Σ, σ(x),...
# Input: chuỗi bất kỳ (string)
# Output: 
#    + True: hợp lệ
#    + False: không hợp lệ  
def check(string):
    result = True
    if len(string) == 1:
        result = False
    else:
        for char in string:
            if char not in alphabet:
                result = False
                break
            
    return result
    

# Tìm tất cả từ phân biệt và tiền xử lý các từ
# Input: list đã tách từ tách câu của vncore, stop word
# Output:  
#    + Dictionary của tất cả từ phân biệt không bao gồm stop word, dấu câu với 
#      key là từ A, value là số lượng từ A có trong văn bản (dict). VD: {hài_hước: 3, 'Bảo_Đại': 5} 
#    + Tổng số từ của văn bản (int)
def total_words_and_len(vncorenlp_postag):
    words = dict()
    doc_len = 0

    for s in vncorenlp_postag:
        for w in s:
            w_temp = w[0].lower()
            doc_len += 1
            if w_temp not in stopwords and check(w_temp) == True:
                if w_temp in words:
                    words[w_temp] += 1
                else:
                    words[w_temp] = 1

    return words, doc_len


# Đếm số câu chứa từ cần check
# Input: từ cần check và list câu của vncore
# Output: số câu chứa từ cần check (int)
def check_word_in_sent(word, vncorenlp_postag):
    count = 0
    for s in vncorenlp_postag:
        if word in s:
            count += 1

    return count


# Lấy n giá trị cao nhất sắp xếp theo thứ tự giảm dần của một dictionary
# Input: Dictionary có chứa giá trị kiểu số để có thể so sánh
# Output: n giá trị cao nhất đã được sắp giảm dần
def get_top(dic, n):
    result = dict(sorted(dic.items(), key = itemgetter(1), reverse = True)[:n]) 
    return result


# Tính giá trị TF của tất cả từ
# Input: Dictionary của tất cả các từ đã tính ở hàm total_word_and_len và tổng số từ của văn bản (đã loại bỏ stopword)
# Output: Giá trị TF của từng từ (dict). VD: {hài_hước: 0.4, 'Bảo_Đại': 0.2} 
def TF(total_words_dict, doc_len):
    tf = dict()
    for key, val in total_words_dict.items():
        tf[key] = val / doc_len
    
    return tf


# Tính giá trị IDF của tất cả từ
# Input: Dictionary của tất cả các từ đã tính ở hàm total_word_and_len và list đã tách từ tách câu của vncore
# Output: Giá trị IDF của từng từ (dict). VD: {hài_hước: 0.01297742362, 'Bảo_Đại': 0.0643231124}
def IDF(total_words_dict, vncorenlp_postag):
    idf = dict()

    for key, val in total_words_dict.items():
        idf[key] = math.log(len(vncorenlp_postag) / (1 + check_word_in_sent(key, vncorenlp_postag)))

    return idf


# Tính giá trị TF-IDF của tất cả từ
# Input: TF (dict) và IDF (dict)
# Output: giá trị TF-IDF (dict)
def TFIDF(tf, idf):
    tfidf = dict()
    tfidf = {key: tf[key] * idf.get(key, 0) for key in tf.keys()}

    return tfidf



# stopwords: Danh sách các stop word. VD: và, là, các, trong, ngoài, của,........
# alphabet: các ký tự hợp lệ như: à, á, ư, b, j, đ, A, Ê, Z, ...... và '_'
stopwords = preprocess_text_file(STOPWORD_FILE_PATH)
alphabet = preprocess_text_file(ALPHABET_FILE_PATH)


def get_link(postag, filename, sentences, numofwords):
    
    words, length = total_words_and_len(postag)

    tf = TF(words, length)
    idf = IDF(words, postag)
    tfidf = TFIDF(tf, idf)
    
    #N giá trị cao nhất
    N = 20
    N_keywords = get_top(tfidf, N)
    #print(N_keywords, '\n')

    kw_index = 0
    keyword_list = list(N_keywords.keys())
    testdata = tag_statistic(keyword_list[kw_index], postag)
    #print(testdata)
    tag = tag_statistic(keyword_list[kw_index], postag)[0][0]

    sentences_index = find_sentence_index(keyword_list[kw_index], tag, postag)

    index = 0
    link = search_keyword(sentences[sentences_index[index]])

    return link

if __name__=='__main__':
    #list_link=p.preprocess_link('docFile_test/bacho.docx')
    a,b,c,d = p.preprocess_link('D:/example.docx')
    l = get_link(a, b, c,d)
    print(l)
