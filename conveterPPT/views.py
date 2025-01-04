from django.shortcuts import render
from django.http import HttpResponse
from .forms import DocumentUploadForm
from docx import Document
from io import BytesIO
from pptx import Presentation  
from pptx.util import Pt, Inches

def process_document_and_create_ppt(request):
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['document']
            document = Document(uploaded_file)
            headings = []
            current_heading = None
            content = []

            for paragraph in document.paragraphs:
                text = paragraph.text.strip()

                
                if text and text.istitle():  
                    if current_heading:
                        headings.append({
                            'title': current_heading,
                            'content': "\n".join(content),
                            'content_paragraphs': content  
                        })
                    current_heading = text
                    content = []
                elif text:  
                    content.append(text)

            if current_heading:
                headings.append({
                    'title': current_heading,
                    'content': "\n".join(content),
                    'content_paragraphs': content  
                })

            presentation = Presentation()
            for heading in headings:
                if heading['title'] and heading['content']:  
                    slide_layout = presentation.slide_layouts[1]  
                    slide = presentation.slides.add_slide(slide_layout)

                    title = slide.shapes.title
                    body = slide.shapes.placeholders[1]
                    title.text = heading['title']
                    title.text_frame.paragraphs[0].font.size = Pt(20)  
                    content_text = heading['content']
                    body.text = content_text
                    for paragraph in body.text_frame.paragraphs:
                        paragraph.font.size = Pt(13)  
                    for i, paragraph in enumerate(heading['content_paragraphs']):
                        text_frame = body.text_frame.paragraphs[i]
                        doc_paragraph = document.paragraphs[i]
                        for run, doc_run in zip(text_frame.runs, doc_paragraph.runs):
                            
                            if hasattr(doc_run, 'bold') and doc_run.bold:
                                run.font.bold = True  
                            else:
                                run.font.bold = False  
                            if hasattr(doc_run, 'italic') and doc_run.italic:
                                run.font.italic = True  
                            else:
                                run.font.italic = False  
                    content_lines = content_text.split("\n")
                    if len(content_lines) > 10:  
                        slide_layout = presentation.slide_layouts[5]  
                        slide = presentation.slides.add_slide(slide_layout)
                        title = slide.shapes.title
                        title.text = heading['title']
                        title.text_frame.paragraphs[0].font.size = Pt(20)  
                        column1 = slide.shapes.add_textbox(left=Inches(0), top=Inches(1), width=Inches(4.5), height=Inches(5))
                        column1_text_frame = column1.text_frame
                        column1_text_frame.text = "\n".join(content_lines[:len(content_lines)//2])
                        for paragraph in column1_text_frame.paragraphs:
                            paragraph.font.size = Pt(13)  
                            for run in paragraph.runs:
                                if hasattr(run, 'bold') and run.bold:
                                    run.font.bold = True  
                                else:
                                    run.font.bold = False  
                                if hasattr(run, 'italic') and run.italic:
                                    run.font.italic = True  
                                else:
                                    run.font.italic = False  

                        column2 = slide.shapes.add_textbox(left=Inches(5), top=Inches(1), width=Inches(4.5), height=Inches(5))
                        column2_text_frame = column2.text_frame
                        column2_text_frame.text = "\n".join(content_lines[len(content_lines)//2:])
                        for paragraph in column2_text_frame.paragraphs:
                            paragraph.font.size = Pt(13)  
                            for run in paragraph.runs:
                                if hasattr(run, 'bold') and run.bold:
                                    run.font.bold = True  
                                else:
                                    run.font.bold = False  
                                if hasattr(run, 'italic') and run.italic:
                                    run.font.italic = True 
                                else:
                                    run.font.italic = False  

            pptx_file = BytesIO()
            presentation.save(pptx_file)  
            pptx_file.seek(0)
            response = HttpResponse(
                pptx_file,
                content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
            response["Content-Disposition"] = 'attachment; filename="document_to_ppt.pptx"'
            return response

    else:
        form = DocumentUploadForm()

    return render(request, 'docUpload.html', {'form': form})
