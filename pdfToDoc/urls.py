from django.urls import path
from .views import convert_pdf_to_word

urlpatterns = [
    path('word/', convert_pdf_to_word, name='convert_pdf_to_word'),
]
