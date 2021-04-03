from django import forms

<<<<<<< HEAD
from .models import DataDocument
=======
from .models import DataDocument, DataDocumentFile
>>>>>>> branch-3--database

#form cho người dùng up 1 file
class DocumentForm(forms.ModelForm):
    class Meta:
        model = DataDocument
        fields = ('DataDocumentName', 'DataDocumentAuthor', 'DataDocumentType', 'DataDocumentFile')

<<<<<<< HEAD
=======
# form cho người dùng up 1 file update fix
class UploadOneFileForm(forms.ModelForm):
    class Meta:
        model = DataDocumentFile
        fields = ['DataDocumentFile']

# form cho người dùng up many file update fix
class UploadManyFileForm(forms.Form):
    
    DataDocumentFile = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

>>>>>>> branch-3--database
class UploadFileForm(forms.Form):
    
    files = forms.FileField()
    title = forms.CharField()
<<<<<<< HEAD
=======
    #test data, do not affect on main flow
class UploadFileFormListVersion(forms.Form):
    
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    title = forms.CharField()
>>>>>>> branch-3--database
