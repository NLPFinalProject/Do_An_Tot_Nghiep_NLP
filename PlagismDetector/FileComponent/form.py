from django import forms
from .models import DataDocument, DataDocumentFile


# form cho người dùng up 1 file
class DocumentForm(forms.ModelForm):
    class Meta:
        model = DataDocument
        fields = ('DataDocumentName', 'DataDocumentAuthor', 'DataDocumentType', 'DataDocumentFile')


# form cho người dùng up 1 file update fix
class UploadOneFileForm(forms.ModelForm):
    class Meta:
        model = DataDocumentFile
        fields = ['DataDocumentFile']


# form cho người dùng up many file
class UploadManyFileForm(forms.Form):
    DataDocumentFile = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))


class UploadFileFormListVersion(forms.Form):
    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
    title = forms.CharField()
