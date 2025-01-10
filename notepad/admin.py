from django.contrib import admin
from .models import Note
# Register your models here.

class NoteAdmin(admin.ModelAdmin):
  fields = ['title','content']

admin.site.register(Note, NoteAdmin)
