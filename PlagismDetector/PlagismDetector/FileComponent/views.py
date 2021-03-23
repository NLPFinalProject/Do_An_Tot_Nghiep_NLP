
"""# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentForm
from rest_framework import status

def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents })


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return Response(uploaded_file_url,status=status.HTTP_200_OK)
        
    return Response('uploaded_file_url',status=status.HTTP_200_OK)


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })"""
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader
from django.urls import reverse
from django.views import generic
from rest_framework.response import Response
from rest_framework import status
#cần import cho db
from .models import DataDocument , DataDocumentContent
from django.db import connection
from django.db.models import Q
#can import cho levenshtein
from .Levenshtein import * 
from PreprocessingComponent.views import *
#cần import cho up file
from django.core.files.storage import FileSystemStorage
from .form import DocumentForm
from .form import UploadFileForm
from django.conf import settings
from PreprocessingComponent import views as p

#import cho tách câu
import os
import sys
sys.path.append(os.getcwd()+'\\polls\\preprocessing')
#from .preprocessing import preprocessor as p
# Create your views here.


# doc code
# rút data từ cursor rồi chuyển về dạng dict
def dictfetchall(cursor): 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

#result
def documentimport(request):
    print('------------------------------')
    # đọc data từ database
    #posts = DataDocumentContent.objects.all()
    cursor = connection.cursor()
    #cursor.execute("SELECT DataDocumentSentence,DataDocumentNo_id  FROM polls_datadocumentcontent WHERE DataDocumentSentence='ABCDEF 123'")
    cursor.execute("SELECT DataDocumentSentence FROM filecomponent_datadocumentcontent WHERE DataDocumentNo_id='1';")
    
    posts = dictfetchall(cursor)
    #list of dicts to list of value (chuyển đổi)
    a_key = "DataDocumentSentence"
    # list 1 lấy từ database
    lst1 = [a_dict[a_key] for a_dict in posts]
    # list 2 user upload, lấy file rồi dùng proccessor, sau đó so sánh

    #doc nhieu file db
    dataReadDoc=[]
    for i in range(1,10):
        try:
            dataFromFile= DataDocument.objects.get(pk=i)
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + dataFromFile.DataDocumentName+ '.'+dataFromFile.DataDocumentType)
            lst2 = lstSentence
            dataReadDoc.append(lst2)
        except Exception:
            pass
    
    dataFromFile= DataDocument.objects.get(pk=1)
    
    fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + dataFromFile.DataDocumentName+ '.'+dataFromFile.DataDocumentType)
    #print(lstSentence)
    lst2 = lstSentence

    #result so sanh
    reportDataReadDoc=[]
    for i in range(len(dataReadDoc)):
        result = Matching_ratio_list(dataReadDoc[i],lst1)
        report = Export(result,dataReadDoc[i],lst1)
        reportDataReadDoc.append(report)
    

    #list of dicts to list of value end
    result = Matching_ratio_list(lst2, lst1)
    report = Export(result, lst2, lst1)

    print(connection.queries)
    print("__________",report)
    return render(request,'polls/output.html',{'data': report})


#upload 1 file
@api_view(('POST',))
def uploadDoc(request):
    content = {'success': 'youre good'}
    if request.method=='POST':
        #print(request.data)
        #filename = request.data['FILES']
        #print('-----file key is'+filekey)
        print('-------------------------------------')
        
        print('-------------------------------------')
        form1 = UploadFileForm(request.POST, request.FILES )
        
        #form1 = UploadFileForm(request.POST,'D:/kamen rider.doc')

        if form1.is_valid():
            # save form người dùng gửi
            data = form1.cleaned_data
            print('yes')
            name2 = data['title'] #abc.doc
            name = str(name2)
            file1 = data['files'] #abc.doc
            
            file_name = name.split(".")[0]#doc
            extension = name.split(".")[-1]#abc
            
            print(file1,type(file1))
            print('-------------------file name is'+file_name)
            print('-------------------extension is'+extension)
            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor="abc",DataDocumentType=extension, DataDocumentFile=file1)
            data.save()
            #data= form1.save(commit = False)
            print('pass')
            # sử dụng preprocessor và lưu vào database
            #lỗi zip file
            """fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)
            
            //save to db//  
            length= len(lstSentence)
            for i in range(length):
                c=data.datadocumentcontentt_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
                print(c)"""
            return Response(content, status=status.HTTP_200_OK)
            ####### fake mocking
        else:
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + 'kamen rider'+'.'+ 'docx')
            
            #//save to db//  
            """data = open("D:\study\PlagismDetector\PlagismDetector\DEF\DocumentFile\\kamen rider.docx")
            length= len(lstSentence)
            for i in range(length):
                c=data.datadocumentcontentt_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
                print(c)"""
            return Response(content, status=status.HTTP_200_OK)
            
    else:
        form = DocumentForm()
    content = {'please move along': 'have the same username'}
    print('fail')
    return Response(content, status=status.HTTP_204_NO_CONTENT)
    
@api_view([ 'GET'])
def test(self):
    main()
    print('done')
    content = {'please move along': 'have the same username222'}
    return Response(content, status=status.HTTP_200_OK)
