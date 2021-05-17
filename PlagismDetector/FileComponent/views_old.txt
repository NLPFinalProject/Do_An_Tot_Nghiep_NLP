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
from .models import *
from django.db import connections, connection
from django.db.models import Q
# can import cho levenshtein
from .levenshtein import *
from PreprocessingComponent.views import *
# cần import cho up file
from django.core.files.storage import FileSystemStorage
# lock command UploadOneFileForm lại trước khi migrations vì sửa dụng model DocumentFile
# from .form import DocumentForm, UploadOneFileForm, UploadManyFileForm
from .form import UploadFileFormListVersion, UploadOneFileForm, UploadManyFileForm
from django.conf import settings
from PreprocessingComponent import views as p
from PreprocessingComponent import TFIDF as internetKeywordSearch
from UserComponent.models import User
# import cho tách câu
import os
import sys
from collections import Counter
import json
import time

numPageSearch = 5
resultRatio = 50
maxFile = 1

rat = 50


# from .preprocessing import preprocessor as p
# Create your views here.


# doc code
# rút data từ cursor rồi chuyển về dạng dict


# result
# them ham tim kiem he thong
# systemSearch
@api_view(('POST',))
def documentimportDatabase(request):
    fileName1 = request.data["filename1"]

    userId = int(request.data["id"])
    # fileName1 = data['fileName1']
    # userId=data['id']

    fileName2Sentence = []

    cursor = connections['default'].cursor()
    # queryRaw ="ALTER TABLE filecomponent_datadocumentcontent ADD FULLTEXT (DataDocumentSentence);"
    # cursor.execute(queryRaw)
    # fileName1
    querys = DataDocument.objects.filter(
        DataDocumentAuthor=str(userId)) \
        .filter(DataDocumentName=fileName1.split(".")[0]) \
        .filter(DataDocumentType=fileName1.split(".")[1])
    fetchQuery = querys[0].DataDocumentFile
    fName, lstSentence, lstLength = p.preprocess(
        settings.MEDIA_ROOT + '/DocumentFile/' + os.path.basename(str(fetchQuery)))
    fileName1Sentence = lstSentence

    # database search
    documentName = []
    documentNameId = []
    for fileSentence in fileName1Sentence:
        sentence = chr(34) + fileSentence.replace(chr(34), "") + chr(34)
        queryRaw = "SELECT id FROM `filecomponent_datadocumentcontent` WHERE MATCH(DataDocumentSentence) Against(" + sentence + ")"
        cursor.execute(queryRaw)
        fetchQuery = dictfetchall(cursor)
        documentNameFind = [a_dict["id"] for a_dict in fetchQuery]
        documentNameId.extend(documentNameFind)
    documentNameId = list(dict.fromkeys(documentNameId))

    for idDoc in documentNameId:
        querys = DataDocumentContent.objects.filter(id=str(idDoc))
        querys = DataDocument.objects.filter(id=querys[0].DataDocumentNo_id)
        documentName.append(str(querys[0].id))

    # thong ke
    idStatistic = Counter(documentName)
    countReport = 0
    reportDataReadDoc = []
    ReportFileName2Sentence = []
    reportIdFile = []
    fileName2 = []
    for idFile in idStatistic.items():
        if (countReport < maxFile):
            querys = DataDocumentContent.objects.filter(DataDocumentNo_id=int(idFile[0])).order_by('id')
            fileName2Sentence = [querys[i].DataDocumentSentence for i in range(len(querys))]
            result = ExportOrder4(fileName1Sentence, fileName2Sentence, resultRatio)
            if (result[1] >= resultRatio and countReport < maxFile):
                countReport += 1
                reportIdFile.append(idFile[0])
                reportDataReadDoc.append(result[0])
                ReportFileName2Sentence.append(fileName2Sentence)
                # querys = DataDocument.objects.filter(id=str(idFile[0]))
                # fileName2Name = querys[0].DataDocumentName
                fileName2Name = str(querys[0].DataDocumentNo)
                fileName2.append(fileName2Name)

    myDict4 = []
    myDict = {}
    # myDict2 = {}
    myDict["File1Name"] = fileName1

    for i in range(countReport):
        mydic3 = {}
        mydic3["data"] = ReportFileName2Sentence[i]
        mydic3["stt"] = reportDataReadDoc[i]
        myDict4.append(mydic3)
        # myDict2[str(reportIdFile[i])] = mydic3

    # line length list
    myDict["ListFileName"] = fileName2
    myDict["ListFile"] = myDict4
    myDict["file1"] = fileName1Sentence
    # myDict["ListFile"].extend(myDictHtml2)

    # myDict["internet"]=myDictHtml2
    return Response(myDict, status=status.HTTP_200_OK)


@api_view(('POST',))
def documentimportDatabaseInternet(request):
    fileName1 = request.data["filename1"]
    userId = int(request.data["id"])

    fileName2Sentence = []

    cursor = connections['default'].cursor()
    # queryRaw ="ALTER TABLE filecomponent_datadocumentcontent ADD FULLTEXT (DataDocumentSentence);"
    # cursor.execute(queryRaw)
    # fileName1
    querys = DataDocument.objects.filter(
        DataDocumentAuthor=str(userId)) \
        .filter(DataDocumentName=fileName1.split(".")[0]) \
        .filter(DataDocumentType=fileName1.split(".")[1])
    fetchQuery = querys[0].DataDocumentFile
    # return tag preprocess
    tagPage, fName, lstSentence, lstLength = p.preprocess_link(
        settings.MEDIA_ROOT + '/DocumentFile/' + os.path.basename(str(fetchQuery)))
    # internet search
    internetPage = internetKeywordSearch.get_link(tagPage, fName, lstSentence, lstLength)
    if (len(internetPage) > numPageSearch):
        internetPage = internetPage[:numPageSearch]
    fileName1Sentence = lstSentence
    # database search
    documentName = []
    documentNameId = []
    for fileSentence in fileName1Sentence:
        sentence = chr(34) + fileSentence.replace(chr(34), "") + chr(34)
        queryRaw = "SELECT id FROM `filecomponent_datadocumentcontent` WHERE MATCH(DataDocumentSentence) Against(" + sentence + ")"
        cursor.execute(queryRaw)
        fetchQuery = dictfetchall(cursor)
        documentNameFind = [a_dict["id"] for a_dict in fetchQuery]
        documentNameId.extend(documentNameFind)

    documentNameId = list(dict.fromkeys(documentNameId))
    for idDoc in documentNameId:
        querys = DataDocumentContent.objects.filter(id=str(idDoc))
        querys = DataDocument.objects.filter(
            id=querys[0].DataDocumentNo_id
        )
        documentName.append(str(querys[0].id))

    # thong ke
    idStatistic = Counter(documentName)
    countReport = 0
    reportDataReadDoc = []
    ReportFileName2Sentence = []
    reportIdFile = []
    fileName2 = []
    for idFile in idStatistic.items():
        if (countReport < maxFile):
            querys = DataDocumentContent.objects.filter(DataDocumentNo_id=int(idFile[0])).order_by('id')
            fileName2Sentence = [querys[i].DataDocumentSentence for i in range(len(querys))]
            result = ExportOrder4(fileName1Sentence, fileName2Sentence, resultRatio)
            if (result[1] >= resultRatio and countReport < maxFile):
                countReport += 1
                reportIdFile.append(idFile[0])
                reportDataReadDoc.append(result[0])
                ReportFileName2Sentence.append(fileName2Sentence)
                # querys = DataDocument.objects.filter(id=str(idFile[0]))
                # fileName2Name = querys[0].DataDocumentName
                fileName2Name = str(querys[0].DataDocumentNo)
                fileName2.append(fileName2Name)

    myDict4 = []
    myDict = {}
    # myDict2 = {}
    myDict["File1Name"] = fileName1

    for i in range(countReport):
        mydic3 = {}
        mydic3["data"] = ReportFileName2Sentence[i]
        mydic3["stt"] = reportDataReadDoc[i]
        myDict4.append(mydic3)
        # myDict2[str(reportIdFile[i])] = mydic3

    # report cac cau html
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

            os.remove(file_pdf)
        else:
            fName = os.path.basename(link)
            lstSentence = internetKeywordSearch.crawl_web(link)
            data = DataDocument(DataDocumentName=link, DataDocumentAuthor_id=userId, DataDocumentType="internet",
                                DataDocumentFile=link)
            data.save()
            dataReadDoc.append(lstSentence)
            # length= len(lstSentence)
            # for i in range(length):
            #     c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=len(lstSentence[i]))

    # B2 trả json
    # result so sanh
    reportDataReadDoc = []
    for i in range(len(dataReadDoc)):
        result = ExportOrder( fileName1Sentence,dataReadDoc[i], rat)
        reportDataReadDoc.append(result)

    myDictHtml2 = []
    fileName2.extend(internetPage)
    for i in range(len(internetPage)):
        mydic3 = {}
        mydic3["data"] = dataReadDoc[i]
        mydic3["stt"] = reportDataReadDoc[i]
        myDictHtml2.append(mydic3)

    # line length list
    myDict["ListFileName"] = fileName2
    myDict["ListFile"] = myDict4
    myDict["file1"] = fileName1Sentence
    myDict["ListFile"].extend(myDictHtml2)

    myDict["internet"] = myDictHtml2
    return Response(myDict, status=status.HTTP_200_OK)


# import mới
# dùng kiểm với data ng dùng
@api_view(('POST', 'GET'))
def documentimport2(request):
    fileName1 = None
    fileName2 = None
    userId = None
    if request.method == 'POST':

        fileName1 = request.data["filename1"]
        fileName2 = request.data["listfile"]
        userId = int(request.data["id"])
    elif request.method == 'GET':
        fileName1 = request.GET.get["filename1"]
        fileName2 = request.GET.get["listfile"]
        userId = int(request.GET.get["id"])
    cursor = connections['default'].cursor()
    # B1 start đọc data từ database
    # fileName1
    # query trên database
    querys = DataDocument.objects.filter(
        DataDocumentAuthor=str(userId)) \
        .filter(DataDocumentName=fileName1.split(".")[0]) \
        .filter(DataDocumentType=fileName1.split(".")[1]
                )
    fetchQuery = querys[0].DataDocumentFile
    fName, lstSentence, lstLength = p.preprocess(
        settings.MEDIA_ROOT + '/DocumentFile/' + os.path.basename(str(fetchQuery)))
    # danh sách các câu trong file1 theo thứ tự
    fileName1Sentence = lstSentence

    # fileName2
    # chạy preprocess cho từng file trong fileName2
    # trả danh sách câu từng file vô dataReadDoc
    # for fileUName in fileName2:
    #     queryRaw = "SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName= '" + \
    #                fileUName.split(".")[0] + "' AND DataDocumentType='" + fileUName.split(".")[
    #                    1] + "' AND DataDocumentAuthor_id=" + str(userId) + ";"
    dataReadDoc = []

    for fileUName in fileName2:
        try:
            # query database
            querys = DataDocument.objects.filter(
                DataDocumentAuthor=str(userId)) \
                .filter(DataDocumentName=fileUName.split(".")[0]) \
                .filter(DataDocumentType=fileUName.split(".")[1])
            fetchQuery = querys[0].DataDocumentFile
            fName, lstSentence, lstLength = p.preprocess(
                settings.MEDIA_ROOT + '/DocumentFile/' + os.path.basename(str(fetchQuery)))
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
        result = ExportOrder(fileName1Sentence,dataReadDoc[i], rat)

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
    return Response(myDict, status=status.HTTP_200_OK)


@api_view(('POST', 'GET'))
def FinalCheck(request):
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
            print('res is ------------------', res)
            return Response(res, status.HTTP_200_OK)
        elif choice == 3:
            print('hohoho')

            res = documentimportInternet2(request.data)
            print('res is ------------------', res)
            return Response(res, status.HTTP_200_OK)
        elif choice == 4:
            res = documentimportInternet2(request.data)
            return Response(res, status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)


# kiểm vs internet
def documentimportInternet2(data):
    fileName1 = data['fileName1']
    userId = data['id']
    cursor = connections['default'].cursor()
    # fileName1
    querys = DataDocument.objects.filter(
        DataDocumentAuthor=str(userId)) \
        .filter(DataDocumentName=fileName1.split(".")[0]) \
        .filter(DataDocumentType=fileName1.split(".")[1])
    fetchQuery = querys[0].DataDocumentFile
    # return tag preprocess
    tagPage, fName, lstSentence, lstLength = p.preprocess_link(
        settings.MEDIA_ROOT + '/DocumentFile/' + os.path.basename(str(fetchQuery)))
    fileName1Sentence = lstSentence

    # internet search
    internetPage = internetKeywordSearch.get_link(tagPage, fName, lstSentence, lstLength)
    if (len(internetPage) > numPageSearch):
        internetPage = internetPage[:numPageSearch]
    print("Link: ", internetPage)
    dataReadDoc = []
    for link in internetPage:
        if (internetKeywordSearch.is_downloadable(link)):
            # link_pdf.append(link)
            file_pdf = internetKeywordSearch.download_document(link)
            fName, lstSentence, lstLength = p.preprocess(file_pdf)
            data = DataDocument(DataDocumentName=os.path.basename(file_pdf), DataDocumentAuthor_id=userId,
                                DataDocumentType="internetPdf", DataDocumentFile=link)
            data.save()
            dataReadDoc.append(lstSentence)
            # length= len(lstSentence)
            # for i in range(length):
            #     c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])

            # os.remove(file_pdf)
        else:
            fName = os.path.basename(link)
            lstSentence = internetKeywordSearch.crawl_web(link)
            data = DataDocument(DataDocumentName=link, DataDocumentAuthor_id=userId, DataDocumentType="internet",
                                DataDocumentFile=link)
            print("length of link: ", len(link))
            data.save()
            dataReadDoc.append(lstSentence)
            # length= len(lstSentence)
            # for i in range(length):
            #     c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=len(lstSentence[i]))
    # B2 trả json
    # result so sánh
    # lần lượt thêm danh sách câu file 1, danh sách câu các file 2, cuối cùng là thứ tự câu so sánh
    # vào reportDataReadDoc
    reportDataReadDoc = []
    # reportDataReadDoc.append(fileName1Sentence)
    # eportDataReadDoc.append(dataReadDoc)
    for i in range(len(dataReadDoc)):
        print("tao report ", i)
        start_time = time.time()
        result = ExportOrder(fileName1Sentence,dataReadDoc[i], rat)
        reportDataReadDoc.append(result)
        print("---tao report ", i, " nay mất %s seconds ---" % (time.time() - start_time))

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

    for i in range(len(internetPage)):
        index = index + 1
        mydic3 = {}

        mydic3["data"] = dataReadDoc[i]
        mydic3["stt"] = reportDataReadDoc[i]
        myDict4.append(mydic3)
    # line length list
    # test mydict function
    listFileName = internetPage
    myDict["ListFileName"] = listFileName
    myDict["File1Name"] = fileName1
    myDict["ListFile"] = myDict4
    # end test
    # FileDatabase=DataDocument.objects.filter(DataDocumentName=fileName1.split(".")[0],DataDocumentType=fileName1.split(".")[1],DataDocumentAuthor_id=str(userId))
    # jsonResult=ReportDocument(DataDocumentName=FileDatabase.,DataDocumentReport=RjsonFile(myDict,fileName1.split(".")[0],userId))
    jsonResult = jsonFile(myDict, fileName1.split(".")[0], userId)

    return myDict


def documentimport(request):
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
    content = None
    if request.method == 'POST':
        id = request.data["id"]

        # filename = request.data['FILES']
        form1 = UploadOneFileForm(request.POST, request.FILES)

        # form1 = UploadFileForm(request.POST,'D:/kamen rider.doc')
        if form1.is_valid():

            # save form người dùng gửi
            data = form1.cleaned_data
            # name2 = data['title'] #abc.doc
            # name = str(name2)
            file1 = data['DataDocumentFile']  # abc.doc

            file_name = file1.name.split(".")[0]  # doc
            extension = file1.name.split(".")[-1]  # abc
            content = file_name
            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=id, DataDocumentType=extension,
                                DataDocumentFile=file1)
            data.save()
            # data= form1.save(commit = False)

            # #lỗi zip file
            # fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)
            # # //save to db//
            # length = len(lstSentence)
            # for i in range(length):
            #     c = data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i],
            #                                             DataDocumentSentenceLength=lstLength[i])

            result = file_name + '.' + extension
            res = result
            content = {'filename': file1}

            return Response(res, status=status.HTTP_200_OK)

            ####### fake mocking
        else:
            # wrong form type
            return Response(content, status=status.HTTP_204_NO_CONTENT)

    else:
        form = UploadOneFileForm()
        content = {'please move along': 'have the same username'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


# upload multiple file
@api_view(('POST', 'GET'))
def uploadDocList(request):
    # chuong trinh test
    content = None
    if request.method == 'POST':
        id = request.data["id"]
        listfile = request.FILES.getlist('DataDocumentFile')
        filenameList = []
        count = 0
        # listname = request.data.getlist('title')
        for f in listfile:
            # name = listname[count]
            count = count + 1
            file1: file
            file1 = f  # abc.doc
            file_name = file1.name.split(".")[0]  # doc
            extension = file1.name.split(".")[-1]  # abc
            filenameList.append(file1.name)

            data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=id, DataDocumentType=extension,
                                DataDocumentFile=file1)
            data.save()
            # # lỗi zip file
            # fName, lstSentence, lstLength = p.preprocess(
            #     settings.MEDIA_ROOT + '\\DocumentFile\\' + data.DataDocumentName + '.' + data.DataDocumentType)
            # # //save to db//
            # length = len(lstSentence)
            # for i in range(length):
            #     c = data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i],
            #                                             DataDocumentSentenceLength=lstLength[i])

        response = {'data': filenameList}

        return JsonResponse(response, status=status.HTTP_200_OK)
    else:
        form = UploadManyFileForm()
        content = {'please move along': 'have the same username'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def test(self):
    main()
    content = {'please move along': 'have the same username222'}
    return Response(content, status=status.HTTP_200_OK)


# from .preprocessing import preprocessor as p
# Create your views here.


# doc code
# rút data từ cursor rồi chuyển về dạng dict
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
            queryRaw = "SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName= '" + \
                       fileName1.split(".")[0] + "' AND DataDocumentType='" + fileName1.split(".")[
                           1] + "' AND DataDocumentAuthor_id=" + str(userId) + ";"
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
            queryRaw = "SELECT DataDocumentFile FROM `filecomponent_datadocument` WHERE DataDocumentName= '" + \
                       fileName1.split(".")[0] + "' AND DataDocumentType='" + fileName1.split(".")[
                           1] + "' AND DataDocumentAuthor_id=" + str(userId) + ";"
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
def jsonFile(request, file_name, userId):
    filename = settings.MEDIA_ROOT + "/result/" + file_name + userId
    print("fullpath:          ", filename)
    mydict = request
    with open(filename + ".json", "w") as f:
        json.dump(mydict, f)
    fileJson = open(filename + ".json", "r")
    reportData = json.loads(fileJson.read())
    print(fileJson.name)
    fileJson.close()
    # os.remove(fileJson.name)
    return fileJson.name


@api_view(['GET'])
def test(self):
    main()
    print('done')
    content = {'please move along': 'have the same username222'}
    return Response(content, status=status.HTTP_200_OK)

# def testting(request):
#     fileName1 = "bacho.docx"
#     userId=3
#     # 1 file access
#     querys = DataDocumentT.objects.filter(
#         DataDocumentAuthor=str(userId)
#         ).filter(
#         DataDocumentName=fileName1.split(".")[0]
#         ).filter(
#         DataDocumentType=fileName1.split(".")[1]
#         )
#     fetchQuery =querys[0].DataDocumentFile
#     print("=======",fetchQuery," ",str(userId)," ",fileName1.split(".")[0]," ",fileName1.split(".")[1])
#
#     # 1 internet link access theo user
#     internetTitle = "cau-6-trang-73-sgk-gdcd-11.jsp"
#     querys = DataDocumentT.objects.filter(DataDocumentType="internet").filter(
#         DataDocumentAuthor=str(userId))\
#         .filter(DataDocumentName=internetTitle)
#     # check all internet link
#     # querys = DataDocumentT.objects.filter(
#     #     DataDocumentType="internet"
#     #     ).filter(
#     #     DataDocumentName=internetTitle
#     #     )
#     fetchQuery =querys[0].DataDocumentFile
#     print("=======",fetchQuery," ",str(userId)," ",fileName1.split(".")[0]," ",fileName1.split(".")[1])
#     # check file exist
#     print("======check=",querys.exists())
#
#     myDict={}
