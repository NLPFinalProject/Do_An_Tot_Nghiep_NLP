
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
#lock command UploadOneFileForm lại trước khi migrations vì sửa dụng model DocumentFile
from .form import DocumentForm, UploadOneFileForm, UploadManyFileForm
from .form import UploadFileForm,UploadFileFormListVersion
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
#import mới
def documentimport2(request):
    print('------------------------------')
    fileName1 = "fileDocC.docx"
    fileName2 = ['fileDocB.docx','vanbanE.docx']
    userId=1

    cursor = connections['default'].cursor()

    #B1 start đọc data từ database
    # fileName1
    #query trên database
    queryRaw ="SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='"+fileName1.split(".")[0]+"' AND DataDocumentAuthor_id='"+str(userId)+"';"
    print("=====",queryRaw)
    cursor.execute(queryRaw)
    fetchQuery = dictfetchall(cursor)
    documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
    print("=====filename1====",os.path.basename(documentNameLink[0]))
    print(settings.MEDIA_ROOT +'\\DocumentFile\\' + os.path.basename(documentNameLink[0]))
    fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile/' + os.path.basename(documentNameLink[0]))
    #danh sách các câu trong file1 theo thứ tự
    fileName1Sentence = lstSentence

    print("===filename2 len ======",len(fileName2),fileName2[1])
    # fileName2
    # chạy preprocess cho từng file trong fileName2
    # trả danh sách câu từng file vô dataReadDoc
    dataReadDoc=[]
    for i in fileName2:
        try:
            #query database
            queryRaw ="SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='"+i.split(".")[0]+"' AND DataDocumentAuthor_id='"+str(userId)+"';"
            cursor.execute(queryRaw)
            
            fetchQuery = dictfetchall(cursor)
            documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
            print("===filename2 ======",os.path.basename(documentNameLink[0]))

            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile/' + os.path.basename(documentNameLink[0]))
            lst2 = lstSentence
            dataReadDoc.append(lst2)
        except Exception:
            pass
    
    #B2 trả json
    # result so sánh
    # lần lượt thêm danh sách câu file 1, danh sách câu các file 2, cuối cùng là thứ tự câu so sánh
    # vào reportDataReadDoc
    reportDataReadDoc=[]
    reportDataReadDoc.append(fileName1Sentence)
    reportDataReadDoc.append(dataReadDoc)
    for i in range(len(dataReadDoc)):
        result = ExportOrder(dataReadDoc[i],fileName1Sentence,30)
        reportDataReadDoc.append(result)
    
    #list of dicts to list of value end

    print(connection.queries)
    return Response(reportDataReadDoc, status=status.HTTP_200_OK)

#import cũ
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


#upload 1 file vo luu tru cau db cua he thong(khac userdb)
def uploadDocumentSentenceToDatabase(request):
    
    if request.method=='POST':
        #print(request.data)
        #filename = request.data['FILES']
        #print('-----file key is'+filekey)
        print('------------------request-------------------')
        
        print('-------------------------------------')
        form1 = UploadOneFileForm(request.POST, request.FILES )
        print(request.FILES)

        if form1.is_valid():
            # save form người dùng gửi
            data = form1.cleaned_data
            print('yes')
            #name2 = data['title'] #abc.doc
            print('-------------------file name2 is',data)
            #name = str(name2)
            file1 = data['DataDocumentFile'] #abc.doc
            print('-------------------file1 is',file1.name)
            file_name = file1.name.split(".")[0]#abc
            extension = file1.name.split(".")[-1]#doc
            
            print(file1,type(file1))
            print('-------------------file name is'+file_name)
            print('-------------------extension is'+extension)

            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=3,DataDocumentType=extension, DataDocumentFile=file1)
            data.save()
            #data= form1.save(commit = False)
            print('pass')
            # sử dụng preprocessor và lưu vào database
            cursor = connections['default'].cursor()
            queryRaw ="SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='"+file_name+"' AND DataDocumentAuthor_id='"+str(3)+"';"
            print("=====",queryRaw)
            cursor.execute(queryRaw)
            fetchQuery = dictfetchall(cursor)
            documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
            print("=====filename1====",os.path.basename(documentNameLink[0]))
            print(settings.MEDIA_ROOT +'\\DocumentFile\\' + os.path.basename(documentNameLink[0]))
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile/' + os.path.basename(documentNameLink[0]))
            
            #fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile/' + data.DataDocumentName+'.'+ data.DataDocumentType)
            
            #//save to db//  
            length= len(lstSentence)
            for i in range(length):
                c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
                print(c)
            return HttpResponseRedirect('http://127.0.0.1:8000/polls/')

        else:
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + 'kamen rider'+'.'+ 'docx')

            return HttpResponseRedirect('http://127.0.0.1:8000/polls/')
            
    else:
        form = UploadOneFileForm()
    #content = {'please move along': 'have the same username'}
    print('fail')
    return render(request,'polls/upload.html',{
        'form':form
    })

#upload multiple file vo luu tru cau db cua he thong(khac userdb)
def uploadMultipleDocumentSentenceToDatabase(request):
    
    if request.method=='POST':
        listfile =  request.FILES.getlist('DataDocumentFile')
        count = 0
        print(request.FILES)
        print('------------------request-------------------')
        print('-------------------listfile is',listfile)
        print('----------------- multiple file --------------------')
        print(request.FILES)

        for f in listfile:
            # save form người dùng gửi
            count = count+1
            file1:file
            file1 = f #abc.doc
            print('-------------------f is',file1)
            file_name = file1.name.split(".")[0]#doc
            extension = file1.name.split(".")[-1]#abc
            
            print(file1,type(file1))
            print('-------------------file name is '+file_name)
            print('-------------------extension is '+extension)

            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=3,DataDocumentType=extension, DataDocumentFile=file1)
            data.save()
            print('pass')

            # sử dụng preprocessor và lưu vào database
            cursor = connections['default'].cursor()
            queryRaw ="SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='"+file_name+"' AND DataDocumentAuthor_id='"+str(3)+"';"
            print("=====",queryRaw)
            cursor.execute(queryRaw)
            fetchQuery = dictfetchall(cursor)
            documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
            print("=====filename1====",os.path.basename(documentNameLink[0]))
            print(settings.MEDIA_ROOT +'\\DocumentFile\\' + os.path.basename(documentNameLink[0]))
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile/' + os.path.basename(documentNameLink[0]))
            
            #//save sentence to db//  
            length= len(lstSentence)
            for i in range(length):
                c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
                print(c)
            return HttpResponseRedirect('http://127.0.0.1:8000/polls/')

        else:
            return HttpResponseRedirect('http://127.0.0.1:8000/polls/')
            
    else:
        form = UploadManyFileForm()
    return render(request,'polls/upload.html',{
        'form':form
    })

#up 1 file vao user db
# uploadDoc3 old -> uploadOneDocUser (change name only)
def uploadOneDocUser(request):
    
    if request.method=='POST':
        #print(request.data)
        #filename = request.data['FILES']
        #print('-----file key is'+filekey)
        print('------------------request-------------------')
        
        print('-------------------------------------')
        form1 = UploadOneFileForm(request.POST, request.FILES )
        print(request.FILES)

        if form1.is_valid():
            # save form người dùng gửi
            data = form1.cleaned_data
            print('yes')
            #name2 = data['title'] #abc.doc
            print('-------------------file name2 is',data)
            #name = str(name2)
            file1 = data['DataDocumentFile'] #abc.doc
            print('-------------------file1 is',file1.name)
            file_name = file1.name.split(".")[0]#doc
            extension = file1.name.split(".")[-1]#abc
            
            print(file1,type(file1))
            print('-------------------file name is'+file_name)
            print('-------------------extension is'+extension)

            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=3,DataDocumentType=extension, DataDocumentFile=file1)
            data.save()
            #data= form1.save(commit = False)
            print('pass')
            # sử dụng preprocessor và lưu vào database

            return HttpResponseRedirect('http://127.0.0.1:8000/polls/')
        else:
            return HttpResponseRedirect('http://127.0.0.1:8000/polls/')
            
    else:
        form = UploadOneFileForm()
    #content = {'please move along': 'have the same username'}
    print('fail')
    return render(request,'polls/upload.html',{
        'form':form
    })

#upload 1 file
@api_view(('POST',))
def uploadDoc(request):
    
    if request.method=='POST':
        #print(request.data)
        #filename = request.data['FILES']
        #print('-----file key is'+filekey)
        print('-------------------------------------')
        
        print('-------------------------------------')
        form1 = UploadOneFileForm(request.POST, request.FILES )
        
        #form1 = UploadFileForm(request.POST,'D:/kamen rider.doc')

        if form1.is_valid():
            # save form người dùng gửi
            data = form1.cleaned_data
            print('yes')
            #name2 = data['title'] #abc.doc
            #name = str(name2)
            file1 = data['DataDocumentFile'] #abc.doc
            
            file_name = file1.name.split(".")[0]#doc
            extension = file1.name.split(".")[-1]#abc
            
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
        form = UploadOneFileForm()
    content = {'please move along': 'have the same username'}
    print('fail')
    return Response(content, status=status.HTTP_204_NO_CONTENT)
    
#upload multiple file
@api_view(('POST',))
def uploadDocList(request):
    #chuong trinh test
    if request.method=='POST':
        listfile =  request.FILES.getlist('DataDocumentFile')
        count = 0
        #listname = request.data.getlist('title')
        print('-------------------listfile is',listfile)
        for f in listfile:

            #name = listname[count]
            count = count+1
            file1:file
            file1 = f #abc.doc
            print('-------------------f is',file1)
            file_name = file1.name.split(".")[0]#doc
            extension = file1.name.split(".")[-1]#abc
            
            print(file1,type(file1))
            print('-------------------file name is '+file_name)
            print('-------------------extension is '+extension)
            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor="abc",DataDocumentType=extension, DataDocumentFile=file1)
            data.save()
            print('stop here right now')
            """fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)
            
            //save to db//  
            length= len(lstSentence)
            for i in range(length):
                c=data.datadocumentcontentt_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
                print(c)"""
        return Response(None, status=status.HTTP_200_OK)    
            
        
        """    
        print(request.data)
        #print(request.data)
        #filename = request.data['FILES']
        #print('-----file key is'+filekey)
        form1 = UploadFileForm(request.POST, request.FILES )
        print(request.FILES)
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
            
            
    else:
        form = UploadManyFileForm()
    content = {'please move along': 'have the same username'}
    print('fail')
    return Response(content, status=status.HTTP_204_NO_CONTENT)"""
    
@api_view([ 'GET'])
def test(self):
    main()
    print('done')
    content = {'please move along': 'have the same username222'}
    return Response(content, status=status.HTTP_200_OK)
