
"""


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
    #get as many file in the database as possible
    maxnumber = 10
    reportDataReadDoc=[]
    for i in range(1,maxnumber):
        try:
            #ko phải get theo pk mà là get theo tên file
            dataFromFile= DataDocument.objects.get(pk=i)
           ####### #begin multi selection
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + dataFromFile.DataDocumentName+ '.'+dataFromFile.DataDocumentType)
            lst2 = lstSentence
            dataReadDoc.append(lst2)
            #begin test
            

            print(connection.queries)
            print("__________",report)
        #end test
        except Exception:
            pass
        #Xử lý danh sách file
    for i in range(len(dataReadDoc)):
                result = Matching_ratio_list(dataReadDoc[i],lst1)
                report = Export(result,dataReadDoc[i],lst1)
                reportDataReadDoc.append(report)
            result = Matching_ratio_list(lst2, lst1)
            report = Export(result, lst2, lst1)
    
#test mock data
def documentimportTestting(request):
    result = {}
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
    result.FileFrom = lst1
    #doc nhieu file db
    dataReadDoc=[]
    listnumber = [1,3,5,7]

    #get as many file in the database as possible
    maxnumber = 10
    reportDataReadDoc=[]
    for i in range(1,maxnumber):
        try:
            dataFromFile= DataDocument.objects.get(pk=i)
           ####### #begin multi selection
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + dataFromFile.DataDocumentName+ '.'+dataFromFile.DataDocumentType)
            lst2 = lstSentence
            dataReadDoc.append(lst2)

            #begin test
            
            for i in range(len(dataReadDoc)):
                result = Matching_ratio_list(dataReadDoc[i],lst1)
                report = ExportResultByJson(result,dataReadDoc[i],lst1, 50)
                reportDataReadDoc.append(report)
            result = Matching_ratio_list(lst2, lst1)
            report = Export(result, lst2, lst1)

            print(connection.queries)
            print("__________",report)
        #end test
        except Exception:
     
            pass
    result.FileTo = dataReadDoc
    data = GodOfModel(fromsentence = lst1,tosentences =dataReadDoc)
    return Response(data=data, status=status.HTTP_200_OK)
    ###################################################list of dicts to list of value end
        
    #begin mock data
    dataFromFile= DataDocument.objects.get(pk=1)
    
    fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + dataFromFile.DataDocumentName+ '.'+dataFromFile.DataDocumentType)
    #print(lstSentence)
    lst2 = lstSentence
    
    #result so sanh
    
    for i in range(len(dataReadDoc)):
        result = Matching_ratio_list(dataReadDoc[i],lst1)
        report = Export(result,dataReadDoc[i],lst1)
        reportDataReadDoc.append(report)
    

    #list of dicts to list of value end
    result = Matching_ratio_list(lst2, lst1)
    report = Export(result, lst2, lst1)

    print(connection.queries)
    print("__________",report)
    return Response(report, status=status.HTTP_200_OK)
    return render(request,'polls/output.html',{'data': report})"""
#upload 1 file

  

from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader
from django.urls import reverse
from django.views import generic
#from rest_framework.response import Response
import json
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework import status
#cần import cho db
from .models import DataDocument , DataDocumentContent
from django.db import connections,connection
from django.db.models import Q
#can import cho levenshtein
from .Levenshtein import * 
from PreprocessingComponent.views import *
#cần import cho up file
from django.core.files.storage import FileSystemStorage
#lock command UploadOneFileForm lại trước khi migrations vì sửa dụng model DocumentFile
#from .form import DocumentForm, UploadOneFileForm, UploadManyFileForm
from .form import UploadFileFormListVersion,UploadOneFileForm,UploadManyFileForm
from django.conf import settings
from PreprocessingComponent import views as p
from PreprocessingComponent import TFIDF as internetKeywordSearch
from UserComponent.models import User
#import cho tách câu
import os
import sys

sys.path.append(os.getcwd()+'\\polls\\preprocessing')
#from .preprocessing import preprocessor as p
# Create your views here.


# doc code
# rút data từ cursor rồi chuyển về dạng dict


#result

#import mới
@api_view(('POST',))
def documentimport2(request):
    print('------------------------------')
    print(request.data)
    
    fileName1 = request.data["filename1"]
    fileName2 = request.data["listfile"]
    userId=int(request.data["id"])
    print(type(fileName2))
    print('file name 1 is ',fileName1)
    print('file name 2 is ',fileName2)
    cursor = connections['default'].cursor()
    print(fileName1.split(".")[0])
    #B1 start đọc data từ database
    # fileName1
    #query trên database
    queryRaw ="SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName= '"+fileName1.split(".")[0]+"' AND DataDocumentAuthor_id="+str(userId)+";"
    print("=====",queryRaw)
    cursor.execute(queryRaw)
    fetchQuery = dictfetchall(cursor)
    print("====fetch======",fetchQuery)
    documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
    print("=====filename1====",os.path.basename(documentNameLink[0]))
    print(settings.MEDIA_ROOT +'\\DocumentFile\\' + os.path.basename(documentNameLink[0]))
    fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile/' + os.path.basename(documentNameLink[0]))
    #danh sách các câu trong file1 theo thứ tự
    fileName1Sentence = lstSentence

    #print("===filename2 len ======",len(fileName2),fileName2[1])
    # fileName2
    # chạy preprocess cho từng file trong fileName2
    # trả danh sách câu từng file vô dataReadDoc
    for i in fileName2:
        print('begin calculate')
        queryRaw ="SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='"+i.split(".")[0]+"' AND DataDocumentAuthor_id="+str(userId)+";"
        print("=========qwery2",queryRaw)
        print(i)
        print('end calculate')
    dataReadDoc=[]
    for i in fileName2:
        try:
            #query database
            queryRaw ="SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='"+i.split(".")[0]+"' AND DataDocumentAuthor_id="+str(userId)+";"
            cursor.execute(queryRaw)
            print("=========qwery2",queryRaw)
            fetchQuery = dictfetchall(cursor)
            documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
            print("===filename2 ======",documentNameLink[0].split("/")[-1])

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
    #reportDataReadDoc.append(fileName1Sentence)
    #eportDataReadDoc.append(dataReadDoc)
    
    for i in range(len(dataReadDoc)):
        result = ExportOrder(fileName1Sentence,dataReadDoc[i],30)
        reportDataReadDoc.append(result)
    
    #list of dicts to list of value end
    # fileName1 = "fileDocA.doc"
    # fileName2 = ['fileDocE.docx','fileDocB.docx']
    # userId=2
    # fileName1Sentence
    
    myDict = {}
    myDict2 = {}

    myDict["file1"] = fileName1Sentence
    myDict4=[]
    listFileName = {}
    index = 0
    
    for i in range(len(fileName2)):
        index = index+1
        print('index is',index)
        mydic3={}

        mydic3["data"]=dataReadDoc[i]
        mydic3["stt"]=reportDataReadDoc[i]
        myDict4.append(mydic3)
        myDict2[fileName2[i]]=mydic3
    #line length list
    # test mydict function
    listFileName=fileName2
    myDict["ListFileName"] = listFileName
    myDict["ListFile"] = myDict4
    #end test
    print("===========",myDict)
    print("++++",dataReadDoc)
    print(connection.queries)
    return Response(myDict, status=status.HTTP_200_OK)

@api_view(('POST',))
def FinalCheck(request):
    print(request.data)
    print(request.data['choice'])
    choice = request.data['choice']
    filename=request.data['id']
    if choice != None:
        print(choice)
        print(type(choice))
        if choice == 1:
            redirect('')
        elif choice == 2:
            print('selection is ',2)
        elif choice == 3:
            print('hohoho')
            
            documentimportInternet2(request.data)
        elif choice == 4: 
            print('selection is ',4)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    return Response( status=status.HTTP_200_OK)
@api_view(['POST','GET'])
def documentimportInternet(request):
    print('------------------------------')
    
    fileName1 = request.data['fileName1']
    userId=request.data['id']

    cursor = connections['default'].cursor()
    # queryRaw ="ALTER TABLE polls_datadocumentcontentt ADD FULLTEXT (DataDocumentSentence);"
    # cursor.execute(queryRaw)
    # fileName1
    queryRaw ="SELECT DataDocumentFile FROM `polls_datadocumentt` WHERE DataDocumentName='"+fileName1.split(".")[0]+"' AND DataDocumentAuthor_id='"+str(userId)+"';"
    print("=====",queryRaw)
    cursor.execute(queryRaw)
    fetchQuery = dictfetchall(cursor)
    documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
    print("=====filename1====",os.path.basename(documentNameLink[0]))
    print(settings.MEDIA_ROOT +'\\DocumentFile/' + os.path.basename(documentNameLink[0]))
    #return tag preprocess
    tagPage,fName,lstSentence,lstLength = p.preprocess_link(settings.MEDIA_ROOT +'\\DocumentFile/' + os.path.basename(documentNameLink[0]))
    print("---tag---",type(tagPage),tagPage)
    #internet search
    internetPage2 = internetKeywordSearch.get_link(tagPage,fName,lstSentence,lstLength)
    fileName1Sentence = lstSentence
    internetPage = [internetPage2[i] for i in range(3)]
    print("_______nội dung report ======== ",internetPage)
    #link_pdf=[]
    #link_html=[]
    # report cac cau html
    dataReadDoc=[]
    for link in internetPage:
        if(internetKeywordSearch.is_downloadable(link)):
            #link_pdf.append(link)
            file_pdf=internetKeywordSearch.download_document(link)
            fName,lstSentence,lstLength = p.preprocess(file_pdf)
            data = DataDocumentT(DataDocumentName=os.path.basename(file_pdf), DataDocumentAuthor_id=3,DataDocumentType="pdf", DataDocumentFile=file_pdf)
            data.save()
            dataReadDoc.append(lstSentence)
            # length= len(lstSentence)
            # for i in range(length):
            #     c=data.datadocumentcontentt_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
            #     print(c)
            
            os.remove(file_pdf)
        else:
            fName=os.path.basename(link)
            lstSentence=internetKeywordSearch.crawl_web(link)
            data = DataDocumentT(DataDocumentName=link, DataDocumentAuthor_id=userId,DataDocumentType="internet", DataDocumentFile=link)
            data.save()
            dataReadDoc.append(lstSentence)
            # length= len(lstSentence)
            # for i in range(length):
            #     c=data.datadocumentcontentt_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=len(lstSentence[i]))
            #     #print(c)
    #B2 trả json
    # result so sanh
    reportDataReadDoc=[]
    for i in range(len(dataReadDoc)):
        result = ExportOrder2(fileName1Sentence, dataReadDoc[i],70)
        reportDataReadDoc.append(result)
    
    #list of dicts to list of value end
    # fileName1 = "fileDocA.doc"
    # fileName2 = ['fileDocE.docx','fileDocB.docx']
    # userId=2
    # fileName1Sentence
    
    myDict = {}
    myDict2 = {}

    myDict["file1"] = fileName1Sentence
    myDict4=[]
    listFileName = {}
    index = 0
    
    for i in range(len(fileName2)):
        index = index+1
        print('index is',index)
        mydic3={}

        mydic3["data"]=dataReadDoc[i]
        mydic3["stt"]=reportDataReadDoc[i]
        myDict4.append(mydic3)
        myDict2[fileName2[i]]=mydic3
    #line length list
    # test mydict function
    listFileName=fileName2
    myDict["ListFileName"] = listFileName
    myDict["ListFile"] = myDict4
    #end test
    print("===========",myDict)
    print("++++",dataReadDoc)
    print(connection.queries)
    return Response(myDict, status=status.HTTP_200_OK)
    #return Response(status=status.HTTP_200_OK)
    #return data(request,'polls/output.html',{'data': internetPage})
#import cũ
def documentimportInternet2(data):
    print('------------------------------')
    print(data)
    fileName1 = data['fileName1']
    userId=data['id']
    print(fileName1)
    cursor = connections['default'].cursor()
    # fileName1
    queryRaw ="SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='"+fileName1.split(".")[0]+"' AND DataDocumentAuthor_id='"+str(userId)+"';"
    print("=====",queryRaw)
    cursor.execute(queryRaw)
    fetchQuery = dictfetchall(cursor)
    documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
    print("=====filename1====",os.path.basename(documentNameLink[0]))
    print(settings.MEDIA_ROOT +'\\DocumentFile/' + os.path.basename(documentNameLink[0]))
    #return tag preprocess
    tagPage,fName,lstSentence,lstLength = p.preprocess_link(settings.MEDIA_ROOT +'\\DocumentFile/' + os.path.basename(documentNameLink[0]))
    fileName1Sentence = lstSentence

    print("---tag---",type(tagPage),tagPage)
    #internet search
    internetPage = internetKeywordSearch.get_link(tagPage,fName,lstSentence,lstLength)

    dataReadDoc=[]
    for link in internetPage:
        if(internetKeywordSearch.is_downloadable(link)):
            #link_pdf.append(link)
            file_pdf=internetKeywordSearch.download_document(link)
            fName,lstSentence,lstLength = p.preprocess(file_pdf)
            data = DataDocument(DataDocumentName=os.path.basename(file_pdf), DataDocumentAuthor_id=3,DataDocumentType="pdf", DataDocumentFile=file_pdf)
            data.save()
            dataReadDoc.append(lstSentence)
            # length= len(lstSentence)
            # for i in range(length):
            #     c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
            #     print(c)
            
            os.remove(file_pdf)
        else:
            fName=os.path.basename(link)
            lstSentence=internetKeywordSearch.crawl_web(link)
            data = DataDocument(DataDocumentName=link, DataDocumentAuthor_id=3,DataDocumentType="internet", DataDocumentFile=link)
            data.save()
            dataReadDoc.append(lstSentence)
            # length= len(lstSentence)
            # for i in range(length):
            #     c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=len(lstSentence[i]))
            #     #print(c)
    #B2 trả json
    # result so sánh
    # lần lượt thêm danh sách câu file 1, danh sách câu các file 2, cuối cùng là thứ tự câu so sánh
    # vào reportDataReadDoc
    reportDataReadDoc=[]
    #reportDataReadDoc.append(fileName1Sentence)
    #eportDataReadDoc.append(dataReadDoc)
    
    for i in range(len(dataReadDoc)):
        result = ExportOrder(fileName1Sentence,dataReadDoc[i],80)
        reportDataReadDoc.append(result)
    
    #list of dicts to list of value end
    # fileName1 = "fileDocA.doc"
    # fileName2 = ['fileDocE.docx','fileDocB.docx']
    # userId=2
    # fileName1Sentence
    print('escape')
    myDict = {}
    myDict2 = {}

    myDict["file1"] = fileName1Sentence
    myDict4=[]
    listFileName = {}
    index = 0
    
    for i in range(len(link_pdf)):
        index = index+1
        print('index is',index)
        mydic3={}

        mydic3["data"]=dataReadDoc[i]
        mydic3["stt"]=reportDataReadDoc[i]
        myDict4.append(mydic3)
        myDict2[fileName2[i]]=mydic3
    #line length list
    # test mydict function
    listFileName=None
    myDict["ListFileName"] = listFileName
    myDict["ListFile"] = myDict4
    #end test
    print("===========",myDict)
    print("++++",dataReadDoc)
    print(connection.queries)
    return Response(myDict, status=status.HTTP_200_OK)
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
    content = None
    if request.method=='POST':
        print(request.data)
        id = request.data["id"]
        
        #print(request.data)
        #filename = request.data['FILES']
        #print('-----file key is'+filekey)
        print('request file is')
        print(request.FILES)
        form1 = UploadOneFileForm(request.POST, request.FILES )
        
        #form1 = UploadFileForm(request.POST,'D:/kamen rider.doc')
        print("-=====---form1",form1)
        if form1.is_valid():

            # save form người dùng gửi
            data = form1.cleaned_data
            print('yes')
            #name2 = data['title'] #abc.doc
            #name = str(name2)
            file1 = data['DataDocumentFile'] #abc.doc
            
            file_name = file1.name.split(".")[0]#doc
            extension = file1.name.split(".")[-1]#abc
            content = file_name
            print(file1,type(file1))
            print('-------------------file name is'+file_name)
            print('-------------------extension is'+extension)
            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=id,DataDocumentType=extension, DataDocumentFile=file1)
            data.save()
            #data= form1.save(commit = False)
            print('pass')
            
            
            #lỗi zip file
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)
            result = file_name +'.'+extension
            res = result
            print(res)
            content = {'filename': file1}
           
            return Response(res, status=status.HTTP_200_OK)
            
            ####### fake mocking
        else:
            #wrong form type
            print('fail')
            return Response(content,status=status.HTTP_204_NO_CONTENT)
            
    else:
        form = UploadOneFileForm()
        content = {'please move along': 'have the same username'}
        print('fail')
        return Response(content, status=status.HTTP_204_NO_CONTENT)
    
#upload multiple file
@api_view(('POST','GET'))
def uploadDocList(request):
    #chuong trinh test
    content = None
    if request.method=='POST':
        print(request.data)
        id = request.data["id"]
        listfile =  request.FILES.getlist('DataDocumentFile')
        filenameList =[]
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
            filenameList.append(file1.name)
            print(file1,type(file1))
            print('-------------------file name is '+file_name)
            
            print('-------------------extension is '+extension)
            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=id,DataDocumentType=extension, DataDocumentFile=file1)
            data.save()
            print('stop here right now')
            
       
        
        response = {'data' : filenameList}
        
        return JsonResponse(response, status=status.HTTP_200_OK)
    else:
        form = UploadManyFileForm()
        content = {'please move along': 'have the same username'}
        print('fail')
        return Response(content, status=status.HTTP_204_NO_CONTENT)
    
@api_view([ 'GET'])
def test(self):
    main()
    print('done')
    content = {'please move along': 'have the same username222'}
    return Response(content, status=status.HTTP_200_OK)  
"""
@api_view(('POST',))
def uploadDoc(request):
    
    if request.method=='POST':
        content = None
        #print(request.data)
        #filename = request.data['FILES']
        #print('-----file key is'+filekey)
        print('-------------------------------------')
        user = User.objects.get(id = 14)
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
            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor=user,DataDocumentType=extension, DataDocumentFile=file1)
            data.save()
            #data= form1.save(commit = False)
            print('pass')
            # sử dụng preprocessor và lưu vào database
            #lỗi zip file
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)
            
            //save to db//  
            length= len(lstSentence)
            for i in range(length):
                c=data.datadocumentcontentt_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
                print(c)
            return Response(content, status=status.HTTP_200_OK)
            ####### fake mocking
        else:
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + 'kamen rider'+'.'+ 'docx')
            
            #//save to db//  
            data = open("D:\study\PlagismDetector\PlagismDetector\DEF\DocumentFile\\kamen rider.docx")
            length= len(lstSentence)
            for i in range(length):
                c=data.datadocumentcontentt_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
                print(c)
            return Response(content, status=status.HTTP_200_OK)
            
    else:
        form = DocumentForm()
    content = {'please move along': 'have the same username'}
    print('fail')
    return Response(content, status=status.HTTP_204_NO_CONTENT)
    
#upload multiple file
@api_view(('POST',))
def uploadDocList(request):
    #chuong trinh test
    if request.method=='POST':
        listfile =  request.FILES.getlist('files')
        count = 0
        listname = request.data.getlist('title')
        id = request.data.id
        user = User.objects.get(id = request.data["id"])
        
        for f in listfile:

            name = listname[count]
            count = count+1
            file1:file
            file1 = f #abc.doc
            
            file_name = name.split(".")[0]#doc
            extension = name.split(".")[-1]#abc
            
            print(file1,type(file1))
            print('-------------------file name is '+file_name)
            print('-------------------extension is '+extension)
            user
            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor="14",DataDocumentType=extension, DataDocumentFile=file1)
            data.save()
            print('stop here right now')
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)
            
            save to db
            length= len(lstSentence)
            for i in range(length):
                c=data.datadocumentcontentt_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
                print(c)
        return Response(None, status=status.HTTP_200_OK)    
            
        
        
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
        form = DocumentForm()
    content = {'please move along': 'have the same username'}
    print('fail')
    return Response(content, status=status.HTTP_204_NO_CONTENT)"""

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
"""def documentimport2(request):
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
    fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + os.path.basename(documentNameLink[0]))
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
            print("===filename2 ======",documentNameLink[0].split("/")[-1])

            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + documentNameLink[0].split("/")[-1])
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
    return Response(reportDataReadDoc, status=status.HTTP_200_OK)"""

#import cũ
"""def documentimport(request):
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
"""

#upload 1 file vo luu tru cau db cua he thong(khac userdb)
def uploadDocumentSentenceToDatabase(request):
    content = None
    if request.method=='POST':
        print(request.data)
        id = request.data["id"]
        
        #print(request.data)
        #filename = request.data['FILES']
        #print('-----file key is'+filekey)
        print('request file is')
        print(request.FILES)
        form1 = UploadOneFileForm(request.POST, request.FILES )
        
        #form1 = UploadFileForm(request.POST,'D:/kamen rider.doc')
        print("-=====---form1",form1)
        if form1.is_valid():

            # save form người dùng gửi
            data = form1.cleaned_data
            print('yes')
            #name2 = data['title'] #abc.doc
            #name = str(name2)
            file1 = data['DataDocumentFile'] #abc.doc
            
            file_name = file1.name.split(".")[0]#doc
            extension = file1.name.split(".")[-1]#abc
            content = file_name
            print(file1,type(file1))
            print('-------------------file name is'+file_name)
            print('-------------------extension is'+extension)
            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=id,DataDocumentType=extension, DataDocumentFile=file1)
            data.save()
            #data= form1.save(commit = False)
            print('pass')
            
            # sử dụng preprocessor và lưu vào database
            cursor = connections['default'].cursor()
            queryRaw ="SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='"+file_name+"' AND DataDocumentAuthor_id='"+str(id)+"';"
            print("=====",queryRaw)
            cursor.execute(queryRaw)
            fetchQuery = dictfetchall(cursor)
            documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
            print("=====filename1====",os.path.basename(documentNameLink[0]))
            print(settings.MEDIA_ROOT +'\\DocumentFile\\' + os.path.basename(documentNameLink[0]))
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile/' + os.path.basename(documentNameLink[0]))
            
            #fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)
            
            #//save to db//  
            length= len(lstSentence)
            for i in range(length):
                c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
                print(c)
            #lỗi zip file
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)
            result = file_name +'.'+extension
            res = result
            print(res)
            content = {'filename': file1}
           
            return Response(res, status=status.HTTP_200_OK)
            
            ####### fake mocking
        else:
            #wrong form type
            print('fail')
            return Response(content,status=status.HTTP_204_NO_CONTENT)
            
    else:
        form = UploadOneFileForm()
        content = {'please move along': 'have the same username'}
        print('fail')
        return Response(content, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def ff(self):
    
    p.docx2txt("D:/project_doc.docx")

#upload multiple file vo luu tru cau db cua he thong(khac userdb)
def uploadMultipleDocumentSentenceToDatabase(request):
    #chuong trinh test
    content = None
    if request.method=='POST':
        print(request.data)
        id = request.data["id"]
        listfile =  request.FILES.getlist('DataDocumentFile')
        filenameList =[]
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
            filenameList.append(file1.name)
            print(file1,type(file1))
            print('-------------------file name is '+file_name)
            
            print('-------------------extension is '+extension)
            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=id,DataDocumentType=extension, DataDocumentFile=file1)
            data.save()
            print('stop here right now')
            
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
            
       
        
        response = {'data' : filenameList}
        
        return JsonResponse(response, status=status.HTTP_200_OK)
    else:
        form = UploadManyFileForm()
        content = {'please move along': 'have the same username'}
        print('fail')
        return Response(content, status=status.HTTP_204_NO_CONTENT)

#up 1 file vao user db
# uploadDoc3 old -> uploadOneDocUser (change name only)


@api_view([ 'GET'])
def test(self):
    main()
    print('done')
    content = {'please move along': 'have the same username222'}
    return Response(content, status=status.HTTP_200_OK)