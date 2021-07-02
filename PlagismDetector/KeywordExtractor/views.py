import math
import time
from operator import itemgetter
import PreprocessingComponent.views as p
from AccessInternet.views import *

# Lower tất cả các từ
# Input: Danh sách các từ (list in list)
# Output: Danh sách từ đã lower (list in list)
def TokenizeLower(tokenize):
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
def PrerpocessTextFile(txt_file):
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
def TotalWords(TokenizeLower):
    words = dict()

    for s in TokenizeLower:
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
def CheckWordInSent(word, tokenize):
    count = 0
    for s in tokenize:
        if word in s:
            count += 1
    return count


# Lấy n giá trị cao nhất sắp xếp theo thứ tự giảm dần của một dictionary
# Input: Dictionary có chứa giá trị kiểu số để có thể so sánh
# Output: n giá trị cao nhất đã được sắp giảm dần
def GetTop(dic, n):
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
def IDF(words, TokenizeLower):
    idf = dict()

    for key, val in words.items():
        idf[key] = math.log(len(TokenizeLower) / (1 + CheckWordInSent(key, TokenizeLower)))

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
#   + TotalWords_dict: Dictionary của tất cả các từ đã tính ở hàm total_word_and_len
#   + Tokenize
#   + TFIDF của tất cả các từ
# Output:
#   + Dictionary có format {Thứ tự câu có tfidf cao nhất: giá trị tfidf của câu, ...}
def SentenceTfIdfVal(TotalWords_dict, tokenize, tfidf):
    valDict = {}

    for i in range(len(tokenize)):
        val = 0
        for w in tokenize[i]:
            if w.lower() in TotalWords_dict:
                val += tfidf[w.lower()]

        valDict[str(i)] = val

    return dict(sorted(valDict.items(), key=itemgetter(1), reverse=True))


# Rút trích cụm từ (gồm n_words từ) có giá trị tfidf cao nhất trong 1 câu
# Số từ có thể lớn hơn n_words vì n_words là số từ hợp lệ trong lúc tính tfidf
# Input:
#   + TotalWords_dict: Dictionary của tất cả các từ đã tính ở hàm total_word_and_len
#   + sentence = [word1, word2, word3,...]
#   + tfidf: TFIDF của tất cả các từ
#   + n_words: Số từ của phrase
def MaxValPhrase(TotalWords_dict, sentence, tfidf, n_words):
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
            if sentence[i].lower() in TotalWords_dict:
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
stopwords = PrerpocessTextFile(STOPWORD_FILE_PATH)
alphabet = PrerpocessTextFile(ALPHABET_FILE_PATH)


def GetLink(sentence, tokenize):
    wordseg = TokenizeLower(tokenize)
    words = TotalWords(wordseg)
    tf = TF(words)
    idf = IDF(words, wordseg)
    tfidf = TFIDF(tf, idf)

    sen_tfidf_val = SentenceTfIdfVal(words, wordseg, tfidf)
    key = list(sen_tfidf_val.keys())

    link = None
    if len(key) != 0:
        for i in range(0, len(key)):
            key[i] = int(key[i])

        sent = sentence[key[0]]
        link = SearchKeyword(sent)

    return link


if __name__ == '__main__':
    FILE_PATH = '.\\testfile\\test.pdf'
    start = time.time()
    filePreprocessed = p.Preprocess(FILE_PATH)
    link = GetLink(filePreprocessed[0], filePreprocessed[1])
    print(link)

    end = time.time()

    print("Time", end - start)
