from django import forms

from .models import DataDocument

#form cho người dùng up 1 file
class DocumentForm(forms.ModelForm):
    class Meta:
        model = DataDocument
        fields = ('DataDocumentName', 'DataDocumentAuthor', 'DataDocumentType', 'DataDocumentFile')

class UploadFileForm(forms.Form):
    
    files = forms.FileField()
    title = forms.CharField()
