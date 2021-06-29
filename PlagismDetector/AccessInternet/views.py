

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
# cần import cho db
from .models import DataDocument , DataDocumentContent
from django.db import connections,connection
from django.db.models import Q
# can import cho levenshtein
from .Levenshtein import * 
from PreprocessingComponent.views import *
# cần import cho up file
from django.core.files.storage import FileSystemStorage
# lock command UploadOneFileForm lại trước khi migrations vì sửa dụng model DocumentFile
# from .form import DocumentForm, UploadOneFileForm, UploadManyFileForm
from .form import UploadFileFormListVersion,UploadOneFileForm,UploadManyFileForm
from django.conf import settings
from PreprocessingComponent import views as p
from PreprocessingComponent import TFIDF as internetKeywordSearch
from UserComponent.models import User
# import cho tách câu
import os
import sys
from collections import Counter
sys.path.append(os.getcwd()+'\\polls\\preprocessing')
# from .preprocessing import preprocessor as p
# Create your views here.


# doc code
# rút data từ cursor rồi chuyển về dạng dict


#result
# them ham tim kiem he thong + internet
#systemSearch
@api_view(('POST',))
def documentimportDatabase(request):
    print('------------------------------')
    fileName1 = request.data["filename1"]        
    userId=int(request.data["id"])
    # fileName1 = data['fileName1']
    # userId=data['id']

    fileName2Sentence = []
    cursor = connections['default'].cursor()
    # queryRaw ="ALTER TABLE filecomponent_datadocumentcontent ADD FULLTEXT (DataDocumentSentence);"
    # cursor.execute(queryRaw)
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
    # print("---tag---",type(tagPage),tagPage)
    #internet search
    internetPage2 = internetKeywordSearch.get_link(tagPage,fName,lstSentence,lstLength)
    fileName1Sentence = lstSentence
    internetPage = [internetPage2[i] for i in range(3)]
    print("_______nội dung report ======== ",internetPage)

    #database search
    documentName=[]
    documentNameId=[]
    for i in fileName1Sentence:
        sentence=chr(34)+i.replace(chr(34),"")+chr(34)
        # print("dbs----",i)
        queryRaw ="SELECT id FROM `filecomponent_datadocumentcontent` WHERE MATCH(DataDocumentSentence) Against(" + sentence +  ")"
        # print("=====",queryRaw)
        cursor.execute(queryRaw)
        fetchQuery = dictfetchall(cursor)
        documentNameFind = [a_dict["id"] for a_dict in fetchQuery]
        documentNameId.extend(documentNameFind)
    
    documentNameId=list(dict.fromkeys(documentNameId))
    for idDoc in documentNameId:
        # print("dbs----",idDoc)
        queryRaw ="SELECT id FROM `filecomponent_datadocument` WHERE id=(SELECT DataDocumentNo_id FROM `filecomponent_datadocumentcontent` WHERE id="+str(idDoc)+");"
        # print("=====",queryRaw)
        cursor.execute(queryRaw)
        fetchQuery = dictfetchall(cursor)
        documentNameFind = [a_dict["id"] for a_dict in fetchQuery]
        documentName.extend(documentNameFind)

    # thong ke
    idStatistic = Counter(documentName)
    countReport = 0
    reportDataReadDoc = []
    ReportFileName2Sentence = []
    reportIdFile = []
    print(idStatistic)
    fileName2=[]
    for idFile in idStatistic.items():
        print(idFile[0])
        if (countReport<1):
            queryRaw ="SELECT DataDocumentSentence FROM `filecomponent_datadocumentcontent` WHERE DataDocumentNo_id="+str(idFile[0])+";"
            print("=====",queryRaw)
            cursor.execute(queryRaw)
            fetchQuery = dictfetchall(cursor)
            fileName2Sentence = [a_dict["DataDocumentSentence"] for a_dict in fetchQuery]
            result = ExportOrder4(fileName2Sentence, fileName1Sentence,10)
            if (result[1]>=10 and countReport<1):
                countReport+=1
                reportIdFile.append(idFile[0])
                reportDataReadDoc.append(result[0])
                ReportFileName2Sentence.append(fileName2Sentence)
                queryRaw ="SELECT DataDocumentName FROM `filecomponent_datadocument` WHERE id="+str(idFile[0])+";"
                print("=====",queryRaw)
                cursor.execute(queryRaw)
                fetchQuery = dictfetchall(cursor)
                fileName2Name = [a_dict["DataDocumentName"] for a_dict in fetchQuery]
                fileName2.append(fileName2Name)
    
    
    
    myDict4=[]
    myDict = {}
    myDict2 = {}
    myDict["File1Name"] = fileName1
    for i in range(countReport):
        mydic3={}
        mydic3["data"]=ReportFileName2Sentence[i]
        mydic3["stt"]=reportDataReadDoc[i]
        myDict4.append(mydic3)
        myDict2[str(reportIdFile[i])]=mydic3
    
    # report cac cau html
    dataReadDoc=[]
    for link in internetPage:
        if(internetKeywordSearch.is_downloadable(link)):
            #link_pdf.append(link)
            file_pdf=internetKeywordSearch.download_document(link)
            fName,lstSentence,lstLength = p.preprocess(file_pdf)
            data = DataDocument(DataDocumentName=os.path.basename(file_pdf), DataDocumentAuthor_id=userId,DataDocumentType="pdf", DataDocumentFile=file_pdf)
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
            data = DataDocument(DataDocumentName=link, DataDocumentAuthor_id=userId,DataDocumentType="internet", DataDocumentFile=link)
            data.save()
            dataReadDoc.append(lstSentence)
            # length= len(lstSentence)
            # for i in range(length):
            #     c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=len(lstSentence[i]))
            #     #print(c)
    
    #B2 trả json
    # result so sanh
    reportDataReadDoc=[]
    for i in range(len(dataReadDoc)):
        result = ExportOrder(fileName1Sentence, dataReadDoc[i],70)
        reportDataReadDoc.append(result)

    myDictHtml2 = []
    fileName2.append(internetPage)
    for i in range(len(internetPage)):
        mydic3={}
        mydic3["data"]=dataReadDoc[i]
        mydic3["stt"]=reportDataReadDoc[i]
        myDictHtml2.append(mydic3)

    #line length list
    myDict["ListFileName"] = fileName2
    myDict["ListFile"]=myDict4
    print(myDict)
    # myDict["internet"]=myDictHtml2
    # print(connection.queries)
    return Response(myDict, status=status.HTTP_200_OK)

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
            data = DataDocument(DataDocumentName=os.path.basename(file_pdf), DataDocumentAuthor_id=userId,DataDocumentType="pdf", DataDocumentFile=file_pdf)
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
            data = DataDocument(DataDocumentName=link, DataDocumentAuthor_id=userId,DataDocumentType="internet", DataDocumentFile=link)
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
    

@api_view([ 'GET'])
def test(self):
    main()
    print('done')
    content = {'please move along': 'have the same username222'}
    return Response(content, status=status.HTTP_200_OK)  


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
            fName, lstSentence, lstLength = p.preprocess(settings.MEDIA_ROOT + '\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)
            result = file_name + '.' + extension
            res = result
            print(res)
            content = {'filename': file1}
            return Response(res, status=status.HTTP_200_OK)            
            # fake mocking
        else:
            #wrong form type
            print('fail')
            return Response(content, status=status.HTTP_204_NO_CONTENT)            
    else:
        form = UploadOneFileForm()
        content = {'please move along': 'have the same username'}
        print('fail')
        return Response(content, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def ff(self):    
    p.docx2txt("D:/project_doc.docx")

# upload multiple file vo luu tru cau db cua he thong(khac userdb)
def uploadMultipleDocumentSentenceToDatabase(request):
    # chuong trinh test
    content = None
    if request.method=='POST':
        print(request.data)
        id = request.data["id"]
        listfile = request.FILES.getlist('DataDocumentFile')
        filenameList = []
        count = 0
        # listname = request.data.getlist('title')
        print('-------------------listfile is', listfile)
        for f in listfile:
            # name = listname[count]
            count = count + 1
            file1: file
            file1 = f #abc.doc
            print('-------------------f is', file1)
            file_name = file1.name.split(".")[0] # doc
            extension = file1.name.split(".")[-1] # abc
            filenameList.append(file1.name)
            print(file1,type(file1))
            print('-------------------file name is '+file_name)
            
            print('-------------------extension is '+extension)
            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=id, DataDocumentType=extension, DataDocumentFile=file1)
            data.save()
            print('stop here right now')            
            # sử dụng preprocessor và lưu vào database
            cursor = connections['default'].cursor()
            queryRaw = "SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='"+file_name+"' AND DataDocumentAuthor_id='"+str(3)+"';"
            print("=====", queryRaw)
            cursor.execute(queryRaw)
            fetchQuery = dictfetchall(cursor)
            documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
            print("=====filename1====", os.path.basename(documentNameLink[0]))
            print(settings.MEDIA_ROOT + '\\DocumentFile\\' + os.path.basename(documentNameLink[0]))
            fName, lstSentence, lstLength = p.preprocess(settings.MEDIA_ROOT + '\\DocumentFile/' + os.path.basename(documentNameLink[0]))
            # //save sentence to db//  
            length = len(lstSentence)
            for i in range(length):
                c = data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
                print(c)
        response = {'data': filenameList}        
        return JsonResponse(response, status=status.HTTP_200_OK)
    else:
        form = UploadManyFileForm()
        content = {'please move along': 'have the same username'}
        print('fail')
        return Response(content, status=status.HTTP_204_NO_CONTENT)

# up 1 file vao user db
# uploadDoc3 old -> uploadOneDocUser (change name only)


@api_view(['GET'])
def test(self):
    main()
    print('done')
    content = {'please move along': 'have the same username222'}
    return Response(content, status=status.HTTP_200_OK)
