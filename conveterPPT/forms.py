from django import forms
from .theme_data import THEMES
class DocumentUploadForm(forms.Form):
    document = forms.FileField()
    theme = forms.ChoiceField(choices=[(key, key.capitalize()) for key in THEMES.keys()])
