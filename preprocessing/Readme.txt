#1/ giải nén file preprocessing.zip
#2/ import module theo các bước:
#	+ trước tiên thêm dòng code thêm đường dẫn tới file preprocessing:


import sys,os
sys.path.insert(1, os.getcwd() + "/preprocessing")
from preprocessing import preprocessor as p
# muốn xử lý file nào thì truyền đường dẫn tuyệt đối của file đó vào

filename, list_sentence, list_numword = p.preprocess("file path")


#filename: tên file
#list_sentence: danh sách các câu
#list_numword: danh sách chiều dài câu