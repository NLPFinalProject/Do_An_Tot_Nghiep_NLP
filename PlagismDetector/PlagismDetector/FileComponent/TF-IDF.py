from operator import itemgetter
import math
import string
#import preprocessor as p
#import internet as i
from googlesearch import search
import requests
import os
from django.conf import settings
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

def search_keyword(keyword):
	list_url=[]
	for url in search(keyword):
	    list_url.append(url)
	return list_url


def download_pdf(list_url):
    res=[]
    for url in list_url:
        if(".pdf" in url):
            if(is_downloadable(url)):
                name=os.path.basename(url)
                r = requests.get(url, allow_redirects=True)
                open(settings.MEDIA_ROOT+"/PDF_Download/"+name, 'wb').write(r.content)
                res.append(settings.MEDIA_ROOT+"/PDF_Download/"+name)

    return res
# vncorenlp_file = 'D:\DH\TotNghiep\core\preprocessing\VnCoreNLP\VnCoreNLP-1.1.1.jar'
# from vncorenlp import VnCoreNLP
# vncorenlp = VnCoreNLP(vncorenlp_file)

def get_path():
    return os.getcwd()

# Cách chạy chương trình:
# Sửa path của các file và thực thi chương trình 

#DOC_FILE_PATH = 'baocao.docx'
STOPWORD_FILE_PATH = 'polls/preprocessing/stopword.txt'
ALPHABET_FILE_PATH = 'polls/preprocessing/alphabet.txt'


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
    print(N_keywords, '\n')

    kw_index = 0
    keyword_list = list(N_keywords.keys())
    tag = tag_statistic(keyword_list[kw_index], postag)[0][0]
    # print(tag_statistic(keyword_list[kw_index], postag))
    sentences_index = find_sentence_index(keyword_list[kw_index], tag, postag)
    for i in sentences_index:
        print(sentences[i], '\n')
    
    index = int(len(sentences_index) / 2)
    link = search_keyword(sentences[sentences_index[index]])

    return link

if __name__=='__main__':
    #list_link=p.preprocess_link('docFile_test/bacho.docx')
    print("list_link")