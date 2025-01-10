from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from django.utils.text import slugify
def notepad(request):
    notes = Note.objects.all()   
    
    return render(request, 'notepad.html', {'notes': notes})

def add_note(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title, content=content)

        return redirect('notepad')
    return render(request, 'add_note.html')

def edit_note(request, slug):
    note = get_object_or_404(Note, slug=slug)
    if request.method == "POST":
        note.title = request.POST['title']
        note.content = request.POST['content']
        note.slug = slugify(note.title) 
        note.save()
        return redirect('notepad')
    return render(request, 'edit_note.html', {'note': note})

def delete_note(request, slug):
    note = get_object_or_404(Note, slug=slug)
    note.delete()
    return redirect('notepad')
def note_details(request, slug):
    note = get_object_or_404(Note, slug=slug)
    return render(request, 'note_details.html', {'note': note})