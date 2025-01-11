from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from django.utils.text import slugify
from weasyprint import HTML
from django.template.loader import render_to_string
import urllib.parse
import os
from django.conf import settings
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
    whatsapp_url = request.build_absolute_uri('/notepad/note/' + slug + '/download-pdf/')
    context = {
        'note': note,
        'whatsapp_url': whatsapp_url,
    }
    return render(request, 'note_details.html', context)

def download_pdf(request, slug):
    try:
        note = Note.objects.get(slug=slug)
        html_string = render_to_string('note_pdf_template.html', {'note': note})
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        # Save the PDF to a file
        pdf_filename = f"{note.slug}.pdf"
        pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)

        # Ensure the folder exists
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(pdf)

        # Return the PDF file as a download
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{note.title}.pdf"'
        return response
    except Note.DoesNotExist:
        return HttpResponse('Note not found', status=404)
    
def share_on_whatsapp(request, note_slug):
    try:
        # Get the note and generate its PDF
        note = Note.objects.get(slug=note_slug)
        pdf_filename = f"{note.slug}.pdf"
        pdf_url = request.build_absolute_uri(f"/media/{pdf_filename}")

        # URL encode the message to send via WhatsApp
        message = f"Check out this note: {pdf_url}"
        whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(message)}"

        return redirect(whatsapp_url)
    except Note.DoesNotExist:
        return HttpResponse('Note not found', status=404)