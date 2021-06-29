from operator import itemgetter
import math
import time
from django.conf import settings
import os
from underthesea import sent_tokenize, word_tokenize
# import PreprocessingComponent.views as p
import PreprocessingComponent.views as p
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from ScrapeSearchEngine.ScrapeSearchEngine import Google,Duckduckgo,Givewater,Bing,Yahoo
import requests
userAgent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
             ' Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68')


# search on google "my user agent"

# check a url can be doawnloaded as a file?
def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    try:
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        return True
    except:
        return False



def search_keyword(search):
    list_url = []
    try:
        list_url.extend(Google(search, userAgent))
    except:
        pass
    try:
        list_url.extend(Bing(search, userAgent))
    except:
        pass
    try:
        list_url.extend(Yahoo(search, userAgent))
    except:
        pass
    try:
        list_url.extend(Duckduckgo(search, userAgent))
    except:
        pass
    try:
        list_url.extend(Givewater(search, userAgent))
    except:
        pass
    return list(dict.fromkeys(list_url))



# download file downloadable such as: pdf, docx,...
def download_document(url):
    if (is_downloadable(url)):
        name = os.path.basename(url)
        r = requests.get(url, allow_redirects=True)
        f = open(settings.MEDIA_ROOT + '\\DocumentFile\\file_downloaded\\' + name, 'wb')
        f.write(r.content)
        return settings.MEDIA_ROOT + '\\DocumentFile\\file_downloaded\\' + name


# crawl text from html website then preprocess and give output: list sentence after preprocessing.
def crawl_web(url):
    try:
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
        temp = text.split("\n")
        for para in temp:
            list_sentence.extend(sent_tokenize(para))
            temp1=p.split_sent_list(list_sentence,450)
            res = [sen.replace("\xa0", "") for sen in temp1]
        return res #list sentence
    except:
        return None

# Lower tất cả các từ
# Input: Danh sách các từ (list in list)
# Output: Danh sách từ đã lower (list in list)
def tokenize_lower(tokenize):
    lst = []

    for sent in tokenize:
        sen = []
        for word in sent:
            sen.append(word.lower())
        lst.append(sen)

    return lst




# Cách chạy chương trình:
# Sửa path của các file và thực thi chương trình

STOPWORD_FILE_PATH = 'PreprocessingComponent/stopword'
ALPHABET_FILE_PATH = 'PreprocessingComponent/alphabet'


# Tách dòng của text và lưu vào mảng
# Input: file .txt
# Output: danh sách các phần tử (list)
def preprocess_text_file(txt_file):
    f = open(txt_file, 'r', encoding='utf-8')
    elements = f.read().split("\n")
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
def total_words(tokenize_lower):
    words = dict()

    for s in tokenize_lower:
        for w in s:
            if w not in stopwords and check(w) == True:
                if w in words:
                    words[w] += 1
                else:
                    words[w] = 1

    return words


# Đếm số câu chứa từ cần check
# Input: từ cần check và list câu. VD [[word1, word2], [word3, word4, word5]]
# Output: số câu chứa từ cần check (int)
def check_word_in_sent(word, tokenize):
    count = 0
    for s in tokenize:
        if word in s:
            count += 1

    return count


# Lấy n giá trị cao nhất sắp xếp theo thứ tự giảm dần của một dictionary
# Input: Dictionary có chứa giá trị kiểu số để có thể so sánh
# Output: n giá trị cao nhất đã được sắp giảm dần
def get_top(dic, n):
    result = dict(sorted(dic.items(), key=itemgetter(1), reverse=True)[:n])
    return result


# Tính giá trị TF của tất cả từ
# Input: Dictionary của tất cả các từ đã tính ở hàm total_word_and_len và tổng số từ của văn bản (đã loại bỏ stopword)
# Output: Giá trị TF của từng từ (dict). VD: {hài_hước: 0.4, 'Bảo_Đại': 0.2}

def TF(words):
    tf = dict()

    for key, val in words.items():
        tf[key] = val / len(words)

    return tf

# Tính giá trị IDF của tất cả từ
# Input: Dictionary của tất cả các từ đã tính ở hàm total_word_and_len và list đã tách từ tách câu
# Output: Giá trị IDF của từng từ (dict). VD: {hài_hước: 0.01297742362, 'Bảo_Đại': 0.0643231124}
def IDF(words, tokenize_lower):
    idf = dict()

    for key, val in words.items():
        idf[key] = math.log(len(tokenize_lower) / (1 + check_word_in_sent(key, tokenize_lower)))

    return idf


# Tính giá trị TF-IDF của tất cả từ
# Input: TF (dict) và IDF (dict)
# Output: giá trị TF-IDF (dict)
def TFIDF(tf, idf):
    tfidf = dict()
    tfidf = {key: tf[key] * idf.get(key, 0) for key in tf.keys()}
    return tfidf


# Tính câu có tổng giá trị TFIDF cao nhất
# Input:
#   + total_words_dict: Dictionary của tất cả các từ đã tính ở hàm total_word_and_len
#   + Tokenize
#   + TFIDF của tất cả các từ
# Output:
#   + Dictionary có format {Thứ tự câu có tfidf cao nhất: giá trị tfidf của câu, ...}
def sentence_tfidf_val(total_words_dict, tokenize, tfidf):
    val_dict = {}

    for i in range(len(tokenize)):
        val = 0
        for w in tokenize[i]:
            if w.lower() in total_words_dict:
                val += tfidf[w.lower()]

        val_dict[str(i)] = val

    return dict(sorted(val_dict.items(), key=itemgetter(1), reverse=True))


# Rút trích cụm từ (gồm n_words từ) có giá trị tfidf cao nhất trong 1 câu
# Số từ có thể lớn hơn n_words vì n_words là số từ hợp lệ trong lúc tính tfidf
# Input:
#   + total_words_dict: Dictionary của tất cả các từ đã tính ở hàm total_word_and_len
#   + sentence = [word1, word2, word3,...]
#   + tfidf: TFIDF của tất cả các từ
#   + n_words: Số từ của phrase
def max_val_phrase(total_words_dict, sentence, tfidf, n_words):
    idx = 0
    max_idx = len(sentence) - n_words

    if n_words > len(sentence):
        return sentence

    phrase = []
    max_val = 0
    while idx <= max_idx:
        value = 0
        phrase_temp = []
        count = 0
        for i in range(idx, len(sentence)):
            if count == n_words:
                break
            if sentence[i].lower() in total_words_dict:
                value += tfidf[sentence[i].lower()]
                count += 1
            phrase_temp.append(sentence[i])

        if value > max_val:
            max_val = value
            phrase = phrase_temp

        idx += 1

    return phrase


# stopwords: Danh sách các stop word. VD: và, là, các, trong, ngoài, của,........
# alphabet: các ký tự hợp lệ như: à, á, ư, b, j, đ, A, Ê, Z, ...... và '_'
stopwords = preprocess_text_file(STOPWORD_FILE_PATH)
alphabet = preprocess_text_file(ALPHABET_FILE_PATH)


def get_link(sentence, tokenize):
    wordseg = tokenize_lower(tokenize)
    words = total_words(wordseg)
    tf = TF(words)
    idf = IDF(words, wordseg)
    tfidf = TFIDF(tf, idf)

    sen_tfidf_val = sentence_tfidf_val(words, wordseg, tfidf)
    key = list(sen_tfidf_val.keys())

    link = None
    if len(key) != 0:
        for i in range(0, len(key)):
            key[i] = int(key[i])

        sent = sentence[key[0]]
        link = search_keyword(sent)

    return link


if __name__ == '__main__':
    FILE_PATH = '.\\testfile\\test.pdf'
    start = time.time()
    file_preprocessed = p.preprocess(FILE_PATH)
    link = get_link(file_preprocessed[1])
    print(link)

    end = time.time()

    print("Time", end - start)
