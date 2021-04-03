from django.db import models
from UserComponent.models import User
# Create your models here.
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class DataDocument(models.Model):
    DataDocumentName = models.CharField(max_length=200)
    DataDocumentType = models.CharField(max_length=10)
<<<<<<< HEAD
    DataDocumentAuthor = models.CharField(max_length=100)
=======
    DataDocumentAuthor = models.ForeignKey(DataDocument, on_delete=models.CASCADE)
>>>>>>> branch-3--database
    DataDocumentFile = models.FileField(upload_to='DocumentFile/')
    def __str__(self):
        return self.DataDocumentName
    def AuthorName(self):
        return self.DataDocumentAuthor
    def DocumentType(self):
        return self.DataDocumentType
<<<<<<< HEAD
=======

#model dùng để tạo form post
#lock command lại trước khi makemigrations
#class này k đưa vào database
#class DataDocumentFile(models.Model):
#    DataDocumentFile = models.FileField(upload_to='DocumentFile/')

>>>>>>> branch-3--database
# nội dung file được tách thành các câu
class DataDocumentContent(models.Model):
    DataDocumentNo = models.ForeignKey(DataDocument, on_delete=models.CASCADE)
    DataDocumentSentence = models.CharField(max_length=200)
    DataDocumentSentenceLength = models.IntegerField(default=0)
    def __str__(self):
        return self.DataDocumentSentence
    def DocName(self):
        return self.DataDocumentNo
    class Meta:
        indexes = [
            models.Index(fields=['DataDocumentNo','DataDocumentSentence'], name='DataDocumentNo_idx'),
            models.Index(fields=['DataDocumentSentence'], name='DataDocumentSentence_idx'),
        ]
