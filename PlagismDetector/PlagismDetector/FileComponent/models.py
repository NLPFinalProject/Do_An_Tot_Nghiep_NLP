from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


#---------model đồ án
class DataDocument(models.Model):
    DataDocumentName = models.CharField(max_length=200)
    DataDocumentType = models.CharField(max_length=10)
    DataDocumentAuthor = models.CharField(max_length=100)
    def __str__(self):
        return self.DataDocumentName
    def AuthorName(self):
        return self.DataDocumentAuthor
    def DocumentType(self):
        return self.DataDocumentType
#file người dùng up post
class DataDocumentT(models.Model):
    DataDocumentName = models.CharField(max_length=200)
    DataDocumentType = models.CharField(max_length=10)
    DataDocumentAuthor = models.CharField(max_length=100)
    DataDocumentFile = models.FileField(upload_to='DocumentFile/')
    def __str__(self):
        return self.DataDocumentName
    def AuthorName(self):
        return self.DataDocumentAuthor
    def DocumentType(self):
        return self.DataDocumentType
# nội dung file được tách thành các câu
class DataDocumentContentT(models.Model):
    DataDocumentNo = models.ForeignKey(DataDocumentT, on_delete=models.CASCADE)
    DataDocumentSentence = models.CharField(max_length=200)
    DataDocumentSentenceLength = models.IntegerField(default=0)
    def __str__(self):
        return self.DataDocumentSentence
    def DocName(self):
        return self.DataDocumentNo
    class Meta:
        indexes = [
            models.Index(fields=['DataDocumentNo','DataDocumentSentence'], name='DataDocumentNoT_idx'),
            models.Index(fields=['DataDocumentSentence'], name='DataDocumentSentenceT_idx'),
        ]

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