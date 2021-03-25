from django import forms

from .models import DataDocumentT

#form cho người dùng up 1 file
class DocumentForm(forms.ModelForm):
    class Meta:
        model = DataDocumentT
        fields = ('DataDocumentName', 'DataDocumentAuthor', 'DataDocumentType', 'DataDocumentFile')