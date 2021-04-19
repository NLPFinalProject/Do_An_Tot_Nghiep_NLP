thêm vào trong setting.py

#vị trí lưu file trong thư mục media
MEDIA_ROOT = os.path.join(BASE_DIR, 'DEF')

MEDIA_URL = '/DEF/'


view.py : các respond sửa lại theo api urls, các chỗ có chữ "polls" sửa lại theo tên app