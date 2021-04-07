thêm 2 hàm mới:
- uploadDocumentSentenceToDatabase
- uploadMultipleDocumentSentenceToDatabase
>> upload 1 và nhiều file đồng thời tách câu và lưu vào database hệ thống
(hiện tại đang cùng chung db với user)

== hàm uploadDoc3(cũ) đổi tên lại thành uploadOneDocUser 
(nội dung hàm uploadOneDocUser(uploadDoc3) k có chỉnh sửa gì vì đã sửa vào đợt trước (1/4), đây là commit lên tạm,
không copy hàm này)


7/4:
- sửa "\\DocumentFile\\" thành "\\DocumentFile/"
- sửa đọc file doc lỗi do module trong preprocessor.py:
	Thêm 2 dòng:
		import pythoncom
    		pythoncom.CoInitialize()
	vào trước :
    		word = win32com.client.Dispatch("Word.application")

