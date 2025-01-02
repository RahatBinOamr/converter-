from django import forms

class DocFileUploadForm(forms.Form):
    doc_file = forms.FileField()
