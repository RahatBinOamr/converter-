from django.shortcuts import render
from .forms import DocFileUploadForm
from .utils import convert_doc_to_excel  
import pandas as pd
def upload_doc(request):
    if request.method == 'POST' and request.FILES['doc_file']:
        form = DocFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc_file = request.FILES['doc_file']
            output_file = convert_doc_to_excel(doc_file)

            df = pd.read_excel(output_file)
            preview_data = df.head(5).to_html(classes='table table-bordered', index=False) 

            return render(request, 'result.html', {'output_file': output_file, 'preview_data': preview_data})
    else:
        form = DocFileUploadForm()
    return render(request, 'upload.html', {'form': form})
