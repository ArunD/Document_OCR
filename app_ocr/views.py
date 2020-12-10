from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from app_ocr.document_parsers.docx_parser import DocxParser
from app_ocr.document_parsers.image_parser import ImageParser
from app_ocr.document_parsers.mail_parser import MailParser
from app_ocr.document_parsers.pdf_parser import PdfParser
import os
import codecs
from Document_OCR.settings import FILE_DIR
import shutil

from Document_OCR.settings import FILE_DIR

# Create your views here.


def save_text_file(text,filename,id):
    if not os.path.isdir(FILE_DIR+'/user_'+id +'/ocrData/'):
        os.mkdir(FILE_DIR+'/user_'+id +'/ocrData/')
    OCR_DIR = FILE_DIR+'/user_'+id +'/ocrData/'
    ocr_path = os.path.join(OCR_DIR,filename + '.txt')
    with codecs.open(ocr_path, 'w','utf-8') as outfile:
        outfile.write(text)
    

@csrf_exempt
def perform_ocr(request):
    print(request.body)
    params = json.loads(request.body)
    document = params['file_name']
    id = params['id']
    id = str(id)
    filename , file_extension = os.path.splitext(document)

    uploaded_path = os.path.join(FILE_DIR,'user_'+id +'/rawData/' + document)
    try :
        #os.mkdir(ANNOTATED_DIR + filename)
        #os.mkdir(FILE_DIR+'/user_'+id +'/htmlData/')
        os.makedirs(FILE_DIR+'/user_'+id +'/htmlData/'+filename)
    except Exception as err:
        print('Mkdir Error : {0}'.format(err))
    TMP_DIR = FILE_DIR+'/user_'+id +'/htmlData/'+filename #os.path.join(ANNOTATED_DIR,filename)
    shutil.copy(uploaded_path , TMP_DIR)
    document_path = os.path.join(TMP_DIR , document)    
    document = open(document_path, 'rb')

    if file_extension in ['.doc', '.docx']:  # os.path.splitext(document.name)[1] in ['.doc', '.docx']: #
        print('Doc file pipeline started')
        parser = DocxParser(TMP_DIR)
    elif file_extension == '.pdf':  # document.content_type == 'application/pdf': #
        print('PDF file pipeline started')
        parser = PdfParser(TMP_DIR)
    elif file_extension in ['.jpg', '.jpeg',
                            '.png']:  # document.content_type in ['image/jpeg', 'image/jpg', 'image/png']: #
        print('jpg file pipeline started')
        parser = ImageParser()
    elif file_extension == '.msg':  # os.path.splitext(document.name)[1] == '.msg': #
        print('msg file pipeline started')
        parser = MailParser(TMP_DIR)
    else:
        print('File format not in list')

    text = parser.parse(document)
    
    save_text_file(text,filename,id)
    
    return JsonResponse(data={'status' : 200})

