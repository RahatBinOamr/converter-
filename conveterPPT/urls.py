from django.urls import path
from .views import process_document_and_create_ppt

urlpatterns = [
    path('ppt', process_document_and_create_ppt, name='ppt'),
]
