from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_doc, name='upload_doc'),
]
