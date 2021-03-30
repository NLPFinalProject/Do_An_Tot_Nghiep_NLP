from operator import itemgetter
import math
import string
from Pdf_extract import read_pages


# Cách chạy chương trình:
# Sửa path của các file và thực thi chương trình 


DOC_FILE_PATH = 'test.pdf'
STOPWORD_FILE_PATH = 'stopword.txt'
ALPHABET_FILE_PATH = 'alphabet.txt'



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
def total_words_and_len(vncorenlp_tokenize, stop_words):
    words = dict()
    doc_len = 0

    for s in vncorenlp_tokenize:
        for w in s:
            w = w.lower()
            doc_len += 1
            if w not in stopwords and check(w) == True:
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



# stopwords: Danh sách các stop word. VD: và, là, các, trong, ngoài, của,........
# alphabet: các ký tự hợp lệ như: à, á, ư, b, j, đ, A, Ê, Z, ...... và '-'
stopwords = preprocess_text_file(STOPWORD_FILE_PATH)
alphabet = preprocess_text_file(ALPHABET_FILE_PATH)

def Main():
    start_page = 1
    end_page = 3
    tokenize = read_pages(start_page, end_page, DOC_FILE_PATH)

    words, len = total_words_and_len(tokenize, stopwords)

    tf = TF(words, len)
    idf = IDF(words, tokenize)
    tfidf = TFIDF(tf, idf)

    # N giá trị cao nhất
    N = 20
    print(get_top(tfidf, N))
    


if __name__ == "__main__":
    Main()
