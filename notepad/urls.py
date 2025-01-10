from django.urls import path
from . import views

urlpatterns = [
    path('notepad/', views.notepad, name='notepad'),
    path('notepad/add/', views.add_note, name='add_note'),
    path('notepad/edit/<slug:slug>/', views.edit_note, name='edit_note'),
    path('notepad/delete/<slug:slug>/', views.delete_note, name='delete_note'),
    path('notepad/note/<slug:slug>/', views.note_details, name='note_details'),  
]
