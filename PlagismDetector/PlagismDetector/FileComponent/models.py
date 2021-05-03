from django.db import models
from UserComponent.models import User
# Create your models here.
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class DataDocument(models.Model):
    DataDocumentName = models.CharField(max_length=1000)
    DataDocumentType = models.CharField(max_length=10)
    DataDocumentAuthor = models.ForeignKey(User, on_delete=models.CASCADE)
    DataDocumentFile = models.FileField(upload_to='DocumentFile/',max_length=1000)
    def __str__(self):
        return self.DataDocumentName
    def AuthorName(self):
        return self.DataDocumentAuthor
    def DocumentType(self):
        return self.DataDocumentType

#model dùng để tạo form post
#lock command lại trước khi makemigrations
#class này k đưa vào database
    def __str__(self):
        return self.DataDocumentSentence
    def DocName(self):
        return self.DataDocumentNo
    class Meta:
        indexes = [
            models.Index(fields=['DataDocumentNo','DataDocumentSentence'], name='DataDocumentNo_idx'),
            models.Index(fields=['DataDocumentSentence'], name='DataDocumentSentence_idx'),
