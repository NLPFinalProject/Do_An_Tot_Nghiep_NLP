from django import forms

from .models import DataDocument, DataDocumentFile

#form cho người dùng up 1 file
class DocumentForm(forms.ModelForm):
    class Meta:
        model = DataDocument
        fields = ('DataDocumentName', 'DataDocumentAuthor', 'DataDocumentType', 'DataDocumentFile')

# form cho người dùng up 1 file update fix
class UploadOneFileForm(forms.ModelForm):
    class Meta:
        model = DataDocumentFile
        fields = ['DataDocumentFile']
class UploadFileForm(forms.Form):
    
    files = forms.FileField()
    title = forms.CharField()
    #test data, do not affect on main flow
class UploadFileFormListVersion(forms.Form):
    
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    title = forms.CharField()
