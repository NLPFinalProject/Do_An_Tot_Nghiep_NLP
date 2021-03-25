from vncorenlp import VnCoreNLP
from operator import itemgetter
import math
import string


# Cách chạy chương trình:
# Sửa path của các file  và thực thi chương trình 
# Chương trình đang trong quá trình hoàn thiện, còn rời rạc nên tạm thời chỉ có thể test bằng file txt


STOPWORD_FILE_PATH = './stopword.txt'
TEXT_FILE_PATH = './test.txt'
VNCORENLP_FILE_PATH = 'VnCoreNLP/VnCoreNLP-1.1.1.jar'



# Danh sách các stop word. VD: và, là, các, trong, ngoài, của,........
stopword_file = open(STOPWORD_FILE_PATH, 'r', encoding='utf-8')
stopwords = stopword_file.readlines()
for i in range(len(stopwords)):
        stopwords[i] = stopwords[i].replace('\n', '')

# Danh sách các dấu câu. VD ? ! . " " { } ( )
punc = string.punctuation
    
stopword_file.close()




# Tìm tất cả từ phân biệt và tiền xử lý các từ
# Input: list đã tách từ tách câu của vncore, list dấu câu (punctuation), stop word
# Output:  
#    + Dictionary của tất cả từ phân biệt không bao gồm stop word, dấu câu với 
#      key là từ A, value là số lượng từ A có trong văn bản (dict). VD: {hài_hước: 3, 'Bảo_Đại': 5} 
#    + Tổng số từ của văn bản (int)
def total_words_and_len(vncorenlp_tokenize, punctuation, stop_words):
    words = dict()
    doc_len = 0

    for s in vncorenlp_tokenize:
        for w in s:
            w = w.lower()
            if w not in punctuation: 
                doc_len += 1
                if w not in stopwords:
                    if w in words:
                        words[w] += 1
                    else:
                        words[w] = 1

    return words, doc_len


# Đếm số câu chứa từ cần check
# Input: từ cần check và list câu của vncore
# Output: số câu chứa từ cần check (int)
def check_word_in_sent(word, vncorenlp_tokenize):
    count = 0
    for s in vncorenlp_tokenize:
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
def IDF(total_words_dict, vncorenlp_tokenize):
    idf = dict()

    for key, val in total_words_dict.items():
        idf[key] = math.log(len(vncorenlp_tokenize) / (1 + check_word_in_sent(key, vncorenlp_tokenize)))

    return idf


# Tính giá trị TF-IDF của tất cả từ
# Input: TF (dict) và IDF (dict)
# Output: giá trị TF-IDF (dict)
def TFIDF(tf, idf):
    tfidf = dict()
    tfidf = {key: tf[key] * idf.get(key, 0) for key in tf.keys()}

    return tfidf



def Main():
    vncorenlp_file = VNCORENLP_FILE_PATH
    vncorenlp = VnCoreNLP(vncorenlp_file)
    
    f = open(TEXT_FILE_PATH, 'r', encoding='utf-8')
    text = f.read()
    f.close()

    tokenize = vncorenlp.tokenize(text)
    words, len = total_words_and_len(tokenize, punc, stopwords)

    tf = TF(words, len)
    idf = IDF(words, tokenize)
    tfidf = TFIDF(tf, idf)

    # N giá trị cao nhất
    N = 20
    print(get_top(tfidf, N))
    


if __name__ == "__main__":
    Main()