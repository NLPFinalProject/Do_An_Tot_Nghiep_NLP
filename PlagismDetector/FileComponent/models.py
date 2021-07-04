from django.db import models

from UserComponent.models import User


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class DataDocument(models.Model):
    DataDocumentName = models.CharField(max_length=1000)
    DataDocumentType = models.CharField(max_length=20)
    DataDocumentAuthor = models.ForeignKey(User, on_delete=models.CASCADE)
    DataDocumentFile = models.FileField(upload_to='DocumentFile/',
                                        max_length=1000)
    SessionId = models.IntegerField(default=0)
    DocumentStatus = models.BooleanField(default=False)  # luu cau vao database

    def __str__(self):
        return self.DataDocumentName

    def AuthorName(self):
        return self.DataDocumentAuthor

    def DocumentType(self):
        return self.DataDocumentType


# model dùng để tạo form post
# lock command lại trước khi makemigrations
# class này k đưa vào database
class DataDocumentFile(models.Model):
    DataDocumentFile = models.FileField(upload_to='DocumentFile/')


# nội dung file được tách thành các câu
# class ReportDocument(models.Model):
#     DataDocumentName=models.ForeignKey(DataDocument,
#     on_delete=models.CASCADE)
#     DataDocumentReport = models.TextField(max_length=700)


class DataDocumentContent(models.Model):
    DataDocumentNo = models.ForeignKey(DataDocument, on_delete=models.CASCADE)
    DataDocumentSentence = models.CharField(max_length=500)
    DataDocumentSentenceLength = models.IntegerField(default=0)

    def __str__(self):
        return self.DataDocumentSentence

    def DocName(self):
        return self.DataDocumentNo

    class Meta:
        indexes = [
            models.Index(fields=['DataDocumentNo', 'DataDocumentSentence'],
                         name='DataDocumentNo_idx'),
            models.Index(fields=['DataDocumentSentence'],
                         name='DataDocumentSentence_idx'),
        ]


class DocumentSession(models.Model):
    NumOfFile = models.IntegerField(default=0)
    Date = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=20, default="Loading")
    SessionUser = models.IntegerField(default=0)
    SessionName = models.CharField(max_length=50, null=True)
    SessionType = models.CharField(max_length=30, null=True)
    ChildReport = models.IntegerField(default=0)


class ReportDocument(models.Model):
    DocumentJson = models.ForeignKey(DataDocument, on_delete=models.CASCADE)
    JsonFile = models.TextField(max_length=700)
