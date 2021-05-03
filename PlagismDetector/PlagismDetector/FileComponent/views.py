
# upload 1 file



from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader
from django.urls import reverse
from django.views import generic
from rest_framework.response import Response
import json
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework import status
# cần import cho db
from .models import DataDocument , DataDocumentContent
from django.db import connections ,connection
from django.db.models import Q
# can import cho levenshtein
from .Levenshtein import *
from PreprocessingComponent.views import *
# cần import cho up file
from django.core.files.storage import FileSystemStorage
# lock command UploadOneFileForm lại trước khi migrations vì sửa dụng model DocumentFile
# from .form import DocumentForm, UploadOneFileForm, UploadManyFileForm
from .form import UploadFileFormListVersion ,UploadOneFileForm ,UploadManyFileForm
from django.conf import settings
from PreprocessingComponent import views as p
from PreprocessingComponent import TFIDF as internetKeywordSearch
from UserComponent.models import User
# import cho tách câu
import os
import sys
from collections import Counter


# from .preprocessing import preprocessor as p
# Create your views here.


# doc code
# rút data từ cursor rồi chuyển về dạng dict


# result
# them ham tim kiem he thong + internet
# systemSearch
@api_view(('POST',))
def documentimportDatabase(request):
    print('------------------------------')
    fileName1 = request.data["filename1"]

    userId =int(request.data["id"])
    # fileName1 = data['fileName1']
    # userId=data['id']

    fileName2Sentence =[]

    cursor = connections['default'].cursor()
    # queryRaw ="ALTER TABLE filecomponent_datadocumentcontent ADD FULLTEXT (DataDocumentSentence);"
    # cursor.execute(queryRaw)
    # fileName1
    queryRaw ="SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='" + \
               fileName1.split(".")[0] + "' AND DataDocumentAuthor_id='" + str(userId) + "';"
    print("=====", queryRaw)
    cursor.execute(queryRaw)
    fetchQuery = dictfetchall(cursor)
    documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
    print("=====filename1====", os.path.basename(documentNameLink[0]))
    print(settings.MEDIA_ROOT + '\\DocumentFile/' + os.path.basename(documentNameLink[0]))
    # return tag preprocess
    tagPage, fName, lstSentence, lstLength = p.preprocess_link(
        settings.MEDIA_ROOT + '\\DocumentFile/' + os.path.basename(documentNameLink[0]))
    # print("---tag---",type(tagPage),tagPage)
    # internet search
    internetPage2 = internetKeywordSearch.get_link(tagPage, fName, lstSentence, lstLength)
    fileName1Sentence = lstSentence
    internetPage = [internetPage2[i] for i in range(3)]
    print("_______nội dung report ======== ", internetPage)

    # database search
    documentName = []
    documentNameId = []
    for i in fileName1Sentence:
        sentence = chr(34) + i.replace(chr(34), "") + chr(34)
        # print("dbs----",i)
        queryRaw = "SELECT id FROM `filecomponent_datadocumentcontent` WHERE MATCH(DataDocumentSentence) Against(" + sentence + ")"
        # print("=====",queryRaw)
        cursor.execute(queryRaw)
        fetchQuery = dictfetchall(cursor)
        documentNameFind = [a_dict["id"] for a_dict in fetchQuery]
        documentNameId.extend(documentNameFind)

    documentNameId = list(dict.fromkeys(documentNameId))
    for idDoc in documentNameId:
        # print("dbs----",idDoc)
        queryRaw = "SELECT id FROM `filecomponent_datadocument` WHERE id=(SELECT DataDocumentNo_id FROM `filecomponent_datadocumentcontent` WHERE id=" + str(
            idDoc) + ");"
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
    fileName2 = []
    for idFile in idStatistic.items():
        print(idFile[0])
        if (countReport < 1):
            queryRaw = "SELECT DataDocumentSentence FROM `filecomponent_datadocumentcontent` WHERE DataDocumentNo_id=" + str(
                idFile[0]) + ";"
            print("=====", queryRaw)
            cursor.execute(queryRaw)
            fetchQuery = dictfetchall(cursor)
            fileName2Sentence = [a_dict["DataDocumentSentence"] for a_dict in fetchQuery]
            result = ExportOrder4(fileName2Sentence, fileName1Sentence, 10)
            if (result[1] >= 10 and countReport < 1):
                countReport += 1
                reportIdFile.append(idFile[0])
                reportDataReadDoc.append(result[0])
                ReportFileName2Sentence.append(fileName2Sentence)
                queryRaw = "SELECT DataDocumentName FROM `filecomponent_datadocument` WHERE id=" + str(idFile[0]) + ";"
                print("=====", queryRaw)
                cursor.execute(queryRaw)
                fetchQuery = dictfetchall(cursor)
                fileName2Name = [a_dict["DataDocumentName"] for a_dict in fetchQuery]
                fileName2.extend(fileName2Name)

    myDict4 = []
    myDict = {}
    myDict2 = {}
    myDict["File1Name"] = fileName1
    for i in range(countReport):
        mydic3 = {}
        mydic3["data"] = ReportFileName2Sentence[i]
        mydic3["stt"] = reportDataReadDoc[i]
        myDict4.append(mydic3)
        myDict2[str(reportIdFile[i])] = mydic3
    # print(myDict4)
    # # report cac cau html
    # dataReadDoc = []
    # for link in internetPage:
    #     if (internetKeywordSearch.is_downloadable(link)):
    #         # link_pdf.append(link)
    #         file_pdf = internetKeywordSearch.download_document(link)
    #         fName, lstSentence, lstLength = p.preprocess(file_pdf)
    #         data = DataDocument(DataDocumentName=os.path.basename(file_pdf), DataDocumentAuthor_id=userId,
    #                             DataDocumentType="pdf", DataDocumentFile=file_pdf)
    #         data.save()
    #         dataReadDoc.append(lstSentence)
    #         # length= len(lstSentence)
    #         # for i in range(length):
    #         #     c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
    #         #     print(c)
    #
    #         os.remove(file_pdf)
    #     else:
    #         fName = os.path.basename(link)
    #         print("start crawl link: ", link, "\n")
    #         lstSentence = internetKeywordSearch.crawl_web(link)
    #         data = DataDocument(DataDocumentName=link, DataDocumentAuthor_id=userId, DataDocumentType="internet",
    #                             DataDocumentFile=link)
    #         data.save()
    #         dataReadDoc.append(lstSentence)
    #         # length= len(lstSentence)
    #         # for i in range(length):
    #         #     c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=len(lstSentence[i]))
    #         #     #print(c)

    # # B2 trả json
    # # result so sanh
    # reportDataReadDoc = []
    # for i in range(len(dataReadDoc)):
    #     result = ExportOrder(fileName1Sentence, dataReadDoc[i], 70)
    #     reportDataReadDoc.append(result)
    #
    # myDictHtml2 = []
    # fileName2.extend(internetPage)
    # for i in range(len(internetPage)):
    #     mydic3 = {}
    #     mydic3["data"] = dataReadDoc[i]
    #     mydic3["stt"] = reportDataReadDoc[i]
    #     myDictHtml2.append(mydic3)

    # line length list
    myDict["ListFileName"] = fileName2
    myDict["ListFile"]=myDict4
    myDict["file1"] = fileName1Sentence
    # myDict["ListFile"].extend(myDictHtml2)

    print(myDict)
    # myDict["internet"]=myDictHtml2
    # print(connection.queries)
    return Response(myDict, status=status.HTTP_200_OK)


# import mới
@api_view(('POST', 'GET'))
def documentimport2(request):
    fileName1 = None
    fileName2 = None
    userId = None
    if request.method == 'POST':
        print('------------------------------')
        print(request.data)

        fileName1 = request.data["filename1"]
        fileName2 = request.data["listfile"]
        userId = int(request.data["id"])
    elif request.method == 'GET':
        print(request.GET)
        fileName1 = request.GET.get["filename1"]
        fileName2 = request.GET.get["listfile"]
        userId = int(request.GET.get["id"])
    print(type(fileName2))
    print('file name 1 is ', fileName1)
    print('file name 2 is ', fileName2)
    cursor = connections['default'].cursor()
    print(fileName1.split(".")[0])
    # B1 start đọc data từ database
    # fileName1
    # query trên database
    queryRaw = "SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName= '" + \
               fileName1.split(".")[0] + "' AND DataDocumentAuthor_id=" + str(userId) + ";"
    print("=====", queryRaw)
    cursor.execute(queryRaw)
    fetchQuery = dictfetchall(cursor)
    print("====fetch======", fetchQuery)
    documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
    print("=====filename1====", os.path.basename(documentNameLink[0]))
    print(settings.MEDIA_ROOT + '\\DocumentFile\\' + os.path.basename(documentNameLink[0]))
    fName, lstSentence, lstLength = p.preprocess(
        settings.MEDIA_ROOT + '\\DocumentFile/' + os.path.basename(documentNameLink[0]))
    # danh sách các câu trong file1 theo thứ tự
    fileName1Sentence = lstSentence

    # print("===filename2 len ======",len(fileName2),fileName2[1])
    # fileName2
    # chạy preprocess cho từng file trong fileName2
    # trả danh sách câu từng file vô dataReadDoc
    for i in fileName2:
        print('begin calculate')
        queryRaw = "SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='" + i.split(".")[
            0] + "' AND DataDocumentAuthor_id=" + str(userId) + ";"
        print("=========qwery2", queryRaw)
        print(i)
        print('end calculate')
    dataReadDoc = []
    for i in fileName2:
        try:
            # query database
            queryRaw = "SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='" + \
                       i.split(".")[0] + "' AND DataDocumentAuthor_id=" + str(userId) + ";"
            cursor.execute(queryRaw)
            print("=========qwery2", queryRaw)
            fetchQuery = dictfetchall(cursor)
            documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
            print("===filename2 ======", documentNameLink[0].split("/")[-1])

            fName, lstSentence, lstLength = p.preprocess(
                settings.MEDIA_ROOT + '\\DocumentFile/' + os.path.basename(documentNameLink[0]))
            lst2 = lstSentence
            dataReadDoc.append(lst2)
        except Exception:
            pass

    # B2 trả json
    # result so sánh
    # lần lượt thêm danh sách câu file 1, danh sách câu các file 2, cuối cùng là thứ tự câu so sánh
    # vào reportDataReadDoc
    reportDataReadDoc = []
    # reportDataReadDoc.append(fileName1Sentence)
    # eportDataReadDoc.append(dataReadDoc)

    for i in range(len(dataReadDoc)):
        result = ExportOrder(fileName1Sentence, dataReadDoc[i], 30)
        reportDataReadDoc.append(result)

    # list of dicts to list of value end
    # fileName1 = "fileDocA.doc"
    # fileName2 = ['fileDocE.docx','fileDocB.docx']
    # userId=2
    # fileName1Sentence

    myDict = {}
    myDict2 = {}

    myDict["file1"] = fileName1Sentence
    myDict4 = []
    listFileName = {}
    index = 0

    for i in range(len(fileName2)):
        index = index + 1
        print('index is', index)
        mydic3 = {}

        mydic3["data"] = dataReadDoc[i]
        mydic3["stt"] = reportDataReadDoc[i]
        myDict4.append(mydic3)
        myDict2[fileName2[i]] = mydic3
    # line length list
    # test mydict function
    listFileName = fileName2
    myDict["ListFileName"] = listFileName
    myDict["ListFile"] = myDict4
    myDict["File1Name"] = fileName1
    # end test
    print("===========", myDict)
    print("++++", dataReadDoc)
    print(connection.queries)
    print(request.method)
    return Response(myDict, status=status.HTTP_200_OK)


@api_view(('POST', 'GET'))
def FinalCheck(request):
    print(request.data)
    print(request.data['choice'])
    choice = request.data['choice']
    filename = request.data['id']
    if choice != None:
        print(choice)
        print(type(choice))
        if choice == 1:
            redirect('')
        elif choice == 2:
            print('selection is ', 2)
            res = documentimportDatabase()
            print('res is ------------------',res)
            return Response(res, status.HTTP_200_OK)
        elif choice == 3:
            print('hohoho')

            res = documentimportInternet2(request.data)
            print('res is ------------------', res)
            return Response(res,status.HTTP_200_OK)
        elif choice == 4:
            res = documentimportInternet2(request.data)
            return Response(res, status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)


def documentimportInternet2(data):
    print('------------------------------')
    print(data)
    fileName1 = data['fileName1']
    userId = data['id']
    print(fileName1)
    cursor = connections['default'].cursor()
    # fileName1
    queryRaw = "SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='" + \
               fileName1.split(".")[0] + "' AND DataDocumentAuthor_id='" + str(userId) + "';"
    print("=====", queryRaw)
    cursor.execute(queryRaw)
    fetchQuery = dictfetchall(cursor)
    documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
    print("=====filename1====", os.path.basename(documentNameLink[0]))
    print(settings.MEDIA_ROOT + '\\DocumentFile/' + os.path.basename(documentNameLink[0]))
    # return tag preprocess
    tagPage, fName, lstSentence, lstLength = p.preprocess_link(
        settings.MEDIA_ROOT + '\\DocumentFile/' + os.path.basename(documentNameLink[0]))
    fileName1Sentence = lstSentence

    print("---tag---", type(tagPage), tagPage)
    # internet search
    internetPage = internetKeywordSearch.get_link(tagPage, fName, lstSentence, lstLength)[:1]
    print(internetPage)
    dataReadDoc = []
    for link in internetPage:
        if (internetKeywordSearch.is_downloadable(link)):
            # link_pdf.append(link)
            file_pdf = internetKeywordSearch.download_document(link)
            fName, lstSentence, lstLength = p.preprocess(file_pdf)
            data = DataDocument(DataDocumentName=os.path.basename(file_pdf), DataDocumentAuthor_id=userId,
                                DataDocumentType="pdf", DataDocumentFile=file_pdf)
            data.save()
            dataReadDoc.append(lstSentence)
            # length= len(lstSentence)
            # for i in range(length):
            #     c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
            #     print(c)

            os.remove(file_pdf)
        else:
            fName = os.path.basename(link)
            lstSentence = internetKeywordSearch.crawl_web(link)
            data = DataDocument(DataDocumentName=link, DataDocumentAuthor_id=userId, DataDocumentType="internet",
                                DataDocumentFile=link)
            data.save()
            dataReadDoc.append(lstSentence)
            print("end craw ",link)
            # length= len(lstSentence)
            # for i in range(length):
            #     c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=len(lstSentence[i]))
            #     #print(c)
    # B2 trả json
    # result so sánh
    # lần lượt thêm danh sách câu file 1, danh sách câu các file 2, cuối cùng là thứ tự câu so sánh
    # vào reportDataReadDoc
    reportDataReadDoc = []
    # reportDataReadDoc.append(fileName1Sentence)
    # eportDataReadDoc.append(dataReadDoc)
    print("tao report")
    for i in range(len(dataReadDoc)):
        result = ExportOrder(fileName1Sentence, dataReadDoc[i], 80)
        reportDataReadDoc.append(result)

    # list of dicts to list of value end
    # fileName1 = "fileDocA.doc"
    # fileName2 = ['fileDocE.docx','fileDocB.docx']
    # userId=2
    # fileName1Sentence
    print('escape')
    myDict = {}
    myDict2 = {}

    myDict["file1"] = fileName1Sentence
    myDict4 = []
    listFileName = {}
    index = 0

    for i in range(len(internetPage)):
        index = index + 1
        print('index is', index)
        mydic3 = {}

        mydic3["data"] = dataReadDoc[i]
        mydic3["stt"] = reportDataReadDoc[i]
        myDict4.append(mydic3)
    # line length list
    # test mydict function
    listFileName = internetPage
    myDict["ListFileName"] = listFileName
    myDict["ListFile"] = myDict4
    # end test
    print("===========", myDict)
    print("++++", dataReadDoc)
    print(connection.queries)
    return myDict


def documentimport(request):
    print('------------------------------')
    # đọc data từ database
    # posts = DataDocumentContent.objects.all()
    cursor = connection.cursor()
    # cursor.execute("SELECT DataDocumentSentence,DataDocumentNo_id  FROM polls_datadocumentcontent WHERE DataDocumentSentence='ABCDEF 123'")
    cursor.execute("SELECT DataDocumentSentence FROM filecomponent_datadocumentcontent WHERE DataDocumentNo_id='1';")

    posts = dictfetchall(cursor)
    # list of dicts to list of value (chuyển đổi)
    a_key = "DataDocumentSentence"
    # list 1 lấy từ database
    lst1 = [a_dict[a_key] for a_dict in posts]
    # list 2 user upload, lấy file rồi dùng proccessor, sau đó so sánh

    # doc nhieu file db
    dataReadDoc = []
    for i in range(1, 10):
        try:
            dataFromFile = DataDocument.objects.get(pk=i)
            fName, lstSentence, lstLength = p.preprocess(
                settings.MEDIA_ROOT + '\\DocumentFile\\' + dataFromFile.DataDocumentName + '.' + dataFromFile.DataDocumentType)
            lst2 = lstSentence
            dataReadDoc.append(lst2)
        except Exception:
            pass

    dataFromFile = DataDocument.objects.get(pk=1)

    fName, lstSentence, lstLength = p.preprocess(
        settings.MEDIA_ROOT + '\\DocumentFile\\' + dataFromFile.DataDocumentName + '.' + dataFromFile.DataDocumentType)
    # print(lstSentence)
    lst2 = lstSentence

    # result so sanh
    reportDataReadDoc = []
    for i in range(len(dataReadDoc)):
        result = Matching_ratio_list(dataReadDoc[i], lst1)
        report = Export(result, dataReadDoc[i], lst1)
        reportDataReadDoc.append(report)

    # list of dicts to list of value end
    result = Matching_ratio_list(lst2, lst1)
    report = Export(result, lst2, lst1)

    print(connection.queries)
    print("__________", report)
    return render(request, 'polls/output.html', {'data': report})


# upload 1 file
@api_view(('POST',))
def uploadDoc(request):
    print('user is')
    print(request.user)
    content = None
    if request.method == 'POST':
        print(request.data)
        id = request.data["id"]

        # print(request.data)
        # filename = request.data['FILES']
        # print('-----file key is'+filekey)
        print('request file is')
        print(request.FILES)
        form1 = UploadOneFileForm(request.POST, request.FILES)

        # form1 = UploadFileForm(request.POST,'D:/kamen rider.doc')
        print("-=====---form1", form1)
        if form1.is_valid():

            # save form người dùng gửi
            data = form1.cleaned_data
            print('yes')
            # name2 = data['title'] #abc.doc
            # name = str(name2)
            file1 = data['DataDocumentFile']  # abc.doc

            file_name = file1.name.split(".")[0]  # doc
            extension = file1.name.split(".")[-1]  # abc
            content = file_name
            print(file1, type(file1))
            print('-------------------file name is' + file_name)
            print('-------------------extension is' + extension)
            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=id, DataDocumentType=extension,
                                DataDocumentFile=file1)
            data.save()
            # data= form1.save(commit = False)
            print('pass')

            # #lỗi zip file
            # fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)
            # # //save to db//
            # length = len(lstSentence)
            # for i in range(length):
            #     c = data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i],
            #                                             DataDocumentSentenceLength=lstLength[i])
            #     # print(c)

            result = file_name + '.' + extension
            res = result
            print(res)
            content = {'filename': file1}

            return Response(res, status=status.HTTP_200_OK)

            ####### fake mocking
        else:
            # wrong form type
            print('fail')
            return Response(content, status=status.HTTP_204_NO_CONTENT)

    else:
        form = UploadOneFileForm()
        content = {'please move along': 'have the same username'}
        print('fail')
        return Response(content, status=status.HTTP_204_NO_CONTENT)


# upload multiple file
@api_view(('POST', 'GET'))
def uploadDocList(request):
    # chuong trinh test
    content = None
    if request.method == 'POST':
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
            file1 = f  # abc.doc
            print('-------------------f is', file1)
            file_name = file1.name.split(".")[0]  # doc
            extension = file1.name.split(".")[-1]  # abc
            filenameList.append(file1.name)
            print(file1, type(file1))
            print('-------------------file name is ' + file_name)

            print('-------------------extension is ' + extension)
            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=id, DataDocumentType=extension,
                                DataDocumentFile=file1)
            data.save()
            print('stop here right now')
            # # lỗi zip file
            # fName, lstSentence, lstLength = p.preprocess(
            #     settings.MEDIA_ROOT + '\\DocumentFile\\' + data.DataDocumentName + '.' + data.DataDocumentType)
            # # //save to db//
            # length = len(lstSentence)
            # for i in range(length):
            #     c = data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i],
            #                                             DataDocumentSentenceLength=lstLength[i])
            #     # print(c)

        response = {'data': filenameList}

        return JsonResponse(response, status=status.HTTP_200_OK)
    else:
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

#upload 1 file
@api_view(('POST',))
def uploadDoc(request):
    content = {'success': 'youre good'}
#import internet pdf
def documentimportInternet(request):
    print('------------------------------')
    fileName1 = "bacho1.doc"
    userId=3

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
            data = DataDocumentT(DataDocumentName=link, DataDocumentAuthor_id=3,DataDocumentType="internet", DataDocumentFile=link)
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

    myDict = {}
    myDict2 = {}
    myDict["file1"] = fileName1Sentence
    for i in range(len(internetPage)):
        mydic3={}
        mydic3["list"+internetPage[i]]=dataReadDoc[i]
        mydic3["stt"]=reportDataReadDoc[i]
        myDict2[internetPage[i]]=mydic3
    #line length list
    myDict["fileName2"]=myDict2
    print(connection.queries)
    return render(request,'polls/output.html',{'data': myDict})

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
        form1 = UploadFileForm(request.POST, request.FILES )
        form1 = UploadOneFileForm(request.POST, request.FILES )
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

        form = DocumentForm()
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
def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


# result
# import mới


# upload 1 file vo luu tru cau db cua he thong(khac userdb)
def uploadDocumentSentenceToDatabase(request):
    content = None
    if request.method == 'POST':
        print(request.data)
        id = request.data["id"]

        # print(request.data)
        # filename = request.data['FILES']
        # print('-----file key is'+filekey)
        print('request file is')
        print(request.FILES)
        form1 = UploadOneFileForm(request.POST, request.FILES)

        # form1 = UploadFileForm(request.POST,'D:/kamen rider.doc')
        print("-=====---form1", form1)
        if form1.is_valid():

            # save form người dùng gửi
            data = form1.cleaned_data
            print('yes')
            # name2 = data['title'] #abc.doc
            # name = str(name2)
            file1 = data['DataDocumentFile']  # abc.doc

            file_name = file1.name.split(".")[0]  # doc
            extension = file1.name.split(".")[-1]  # abc
            content = file_name
            print(file1, type(file1))
            print('-------------------file name is' + file_name)
            print('-------------------extension is' + extension)
            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=id, DataDocumentType=extension,
                                DataDocumentFile=file1)
            data.save()
            # data= form1.save(commit = False)
            print('pass')

            # sử dụng preprocessor và lưu vào database
            cursor = connections['default'].cursor()
            queryRaw = "SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='" + file_name + "' AND DataDocumentAuthor_id='" + str(
                id) + "';"
            print("=====", queryRaw)
            cursor.execute(queryRaw)
            fetchQuery = dictfetchall(cursor)
            documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
            print("=====filename1====", os.path.basename(documentNameLink[0]))
            print(settings.MEDIA_ROOT + '\\DocumentFile\\' + os.path.basename(documentNameLink[0]))
            fName, lstSentence, lstLength = p.preprocess(
                settings.MEDIA_ROOT + '\\DocumentFile/' + os.path.basename(documentNameLink[0]))

            # fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)

            # //save to db//
            length = len(lstSentence)
            for i in range(length):
                c = data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i],
                                                        DataDocumentSentenceLength=lstLength[i])
                print(c)
            # lỗi zip file
            fName, lstSentence, lstLength = p.preprocess(
                settings.MEDIA_ROOT + '\\DocumentFile\\' + data.DataDocumentName + '.' + data.DataDocumentType)
            result = file_name + '.' + extension
            res = result
            print(res)
            content = {'filename': file1}

            return Response(res, status=status.HTTP_200_OK)

            ####### fake mocking
        else:
            # wrong form type
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
    if request.method == 'POST':
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
            file1 = f  # abc.doc
            print('-------------------f is', file1)
            file_name = file1.name.split(".")[0]  # doc
            extension = file1.name.split(".")[-1]  # abc
            filenameList.append(file1.name)
            print(file1, type(file1))
            print('-------------------file name is ' + file_name)

            print('-------------------extension is ' + extension)
            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=id, DataDocumentType=extension,
                                DataDocumentFile=file1)
            data.save()
            print('stop here right now')

            # sử dụng preprocessor và lưu vào database
            cursor = connections['default'].cursor()
            queryRaw = "SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName='" + file_name + "' AND DataDocumentAuthor_id='" + str(
                3) + "';"
            print("=====", queryRaw)
            cursor.execute(queryRaw)
            fetchQuery = dictfetchall(cursor)
            documentNameLink = [a_dict["DataDocumentFile"] for a_dict in fetchQuery]
            print("=====filename1====", os.path.basename(documentNameLink[0]))
            print(settings.MEDIA_ROOT + '\\DocumentFile\\' + os.path.basename(documentNameLink[0]))
            fName, lstSentence, lstLength = p.preprocess(
                settings.MEDIA_ROOT + '\\DocumentFile/' + os.path.basename(documentNameLink[0]))

            # //save sentence to db//
            length = len(lstSentence)
            for i in range(length):
                c = data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i],
                                                        DataDocumentSentenceLength=lstLength[i])
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

