from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.http import Http404
from rest_framework.response import Response
import json
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework import status
# cần import cho db
from .models import DataDocument, DataDocumentContent
from django.db import connections, connection
# can import cho levenshtein
from .levenshtein import ExportOrder, ExportOrder4
from PreprocessingComponent.views import *
# cần import cho up file
from django.core.files.storage import FileSystemStorage
from .form import UploadOneFileForm, UploadManyFileForm
from django.conf import settings
from PreprocessingComponent import views as p
from PreprocessingComponent import TFIDF as internetKeywordSearch
# import cho tách câu
import os
from collections import Counter
# import json

numPageSearch = 5
resultRatio = 50
maxFile = 1
rat = 50


# check agree
def checkAgree(status, data):
    agreeStatus = status
    if (agreeStatus):
        fName, lstSentence, lstLength = p.preprocess(
            formatString(
                'DocumentFile',
                data.DataDocumentName,
                data.DataDocumentType))
        # //save to db//
        length = len(lstSentence)
        for i in range(length):
            data.datadocumentcontent_set.create(
                DataDocumentSentence=lstSentence[i],
                DataDocumentSentenceLength=lstLength[i])
        return fName
    else:
        return 0


# format string
# folder = DocumentFile
# fileName = filename
# extension = extension
def formatString(folder, fileName, extension):
    FileString = "{base}\\{folder}\\{fileName}.{extension}"
    FileString.format(
        base=settings.MEDIA_ROOT,
        folder=folder,
        fileName=fileName,
        extension=extension)
    return FileString


# format query
# folder = DocumentFile
# fileName = filename
def formatQuery(folder, fileName):
    FileString = "{base}\\{folder}\\{fileName}"
    FileString.format(
        base=settings.MEDIA_ROOT,
        folder=folder,
        fileName=fileName)
    return FileString


# format raw
# folder = DocumentFile
# fileName = filename
# extension = extension
def formatRaw(sentence):
    queryString = "SELECT id FROM `filecomponent_datadocumentcontent`" + \
        "WHERE MATCH(DataDocumentSentence) AGAINST({sentence})"
    queryString.format(
        sentence=sentence)
    return queryString


# database search
def databaseSearch(fileName1Sentence):
    documentName = []
    documentNameId = []
    cursor = connections['default'].cursor()
    for fileSentence in fileName1Sentence:
        sentence = chr(34) + fileSentence.replace(chr(34), "") + chr(34)
        queryRaw = formatRaw(sentence)
        cursor.execute(queryRaw)
        fetchQuery = dictfetchall(cursor)
        documentNameFind = [a_dict["id"] for a_dict in fetchQuery]
        documentNameId.extend(documentNameFind)
    documentNameId = list(dict.fromkeys(documentNameId))

    for idDoc in documentNameId:
        querys = DataDocumentContent.objects.filter(id=str(idDoc))
        querys = DataDocument.objects.filter(id=querys[0].DataDocumentNo_id)
        documentName.append(str(querys[0].id))
    return documentName


def makeDataReadDoc(internetPage, userId):
    dataReadDoc = []
    for link in internetPage:
        if (internetKeywordSearch.is_downloadable(link)):
            # link_pdf.append(link)
            file_pdf = internetKeywordSearch.download_document(link)
            fName, lstSentence, lstLength = p.preprocess(file_pdf)
            data = DataDocument(
                DataDocumentName=os.path.basename(file_pdf),
                DataDocumentAuthor_id=userId,
                DataDocumentType="internetPdf",
                DataDocumentFile=link
                )
            data.save()
            dataReadDoc.append(lstSentence)
            length = len(lstSentence)
            for i in range(length):
                data.datadocumentcontent_set.create(
                    DataDocumentSentence=lstSentence[i],
                    DataDocumentSentenceLength=lstLength[i])

            os.remove(file_pdf)
        else:
            fName = os.path.basename(link)
            lstSentence = internetKeywordSearch.crawl_web(fName)
            data = DataDocument(
                DataDocumentName=fName,
                DataDocumentAuthor_id=userId,
                DataDocumentType="internet",
                DataDocumentFile=fName
                )
            data.save()
            dataReadDoc.append(lstSentence)
            length = len(lstSentence)
            for i in range(length):
                data.datadocumentcontent_set.create(
                    DataDocumentSentence=lstSentence[i],
                    DataDocumentSentenceLength=len(lstSentence[i]))
    return dataReadDoc


def makeData(countReport, ReportFileName2Sentence, reportDataReadDoc):
    myDict4 = []
    for i in range(countReport):
        mydic3 = {}
        mydic3["data"] = ReportFileName2Sentence[i]
        mydic3["stt"] = reportDataReadDoc[i]
        myDict4.append(mydic3)
    return myDict4


# result
# systemSearch
@api_view(('POST',))
def documentimportDatabase(request):
    # fileName1 = request.data["filename1"]
    # userId = int(request.data["id"])
    data1 = request.data
    myDict = test1(data1)
    return Response(myDict, status=status.HTTP_200_OK)


@api_view(('POST',))
def documentimportDatabaseInternet(request):
    # fileName1 = request.data["fileName1"]
    # userId = int(request.data["id"])
    data1 = request.data
    myDict1 = test1(data1)
    myDict2 = test2(data1)
    myDict = []
    myDict.append(myDict1)
    myDict.append(myDict2)
    return Response(myDict, status=status.HTTP_200_OK)


def test1(data):
    fileName1 = data["filename1"]
    userId = int(data["id"])
    fileName2Sentence = []
    # cursor = connections['default'].cursor()
    # fileName1
    querys = DataDocument.objects.filter(
        DataDocumentAuthor=str(userId)) \
        .filter(DataDocumentName=fileName1.split(".")[0]) \
        .filter(DataDocumentType=fileName1.split(".")[1])
    fetchQuery = querys[0].DataDocumentFile
    fName, lstSentence, lstLength = p.preprocess(
        formatQuery('DocumentFile', os.path.basename(str(fetchQuery))))
    fileName1Sentence = lstSentence

    # database search
    documentName = databaseSearch(fileName1Sentence)

    # thong ke
    idStatistic = Counter(documentName)
    countReport = 0
    reportDataReadDoc = []
    ReportFileName2Sentence = []
    reportIdFile = []
    fileName2 = []
    for idFile in idStatistic.items():
        if (countReport < maxFile):
            querys = DataDocumentContent.objects.filter(
                DataDocumentNo_id=int(idFile[0])).order_by('id')
            fileName2Sentence = [
                querys[i].DataDocumentSentence for i in range(len(querys))]
            result = ExportOrder4(
                fileName1Sentence, fileName2Sentence, resultRatio)
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
    myDict["File1Name"] = fileName1
    myDict4 = makeData(countReport, ReportFileName2Sentence, reportDataReadDoc)

    # line length list
    myDict["ListFileName"] = fileName2
    myDict["ListFile"] = myDict4
    myDict["file1"] = fileName1Sentence

    return myDict


def test2(data):
    fileName1 = data['fileName1']
    userId = data['id']
    # cursor = connections['default'].cursor()
    # fileName1
    querys = DataDocument.objects.filter(
        DataDocumentAuthor=str(userId)) \
        .filter(DataDocumentName=fileName1.split(".")[0]) \
        .filter(DataDocumentType=fileName1.split(".")[1])
    fetchQuery = querys[0].DataDocumentFile
    # return tag preprocess
    tagPage, fName, lstSentence, lstLength = p.preprocess_link(
        formatQuery('DocumentFile', os.path.basename(str(fetchQuery))))
    fileName1Sentence = lstSentence

    # internet search
    internetPage = internetKeywordSearch.get_link(
        tagPage, fName, lstSentence, lstLength)
    if (len(internetPage) > numPageSearch):
        internetPage = internetPage[:numPageSearch]
    print("Link: ", internetPage)
    dataReadDoc = makeDataReadDoc(internetPage, userId)

    # B2 trả json
    reportDataReadDoc = []
    for i in range(len(dataReadDoc)):
        result = ExportOrder(fileName1Sentence, dataReadDoc[i], rat)
        reportDataReadDoc.append(result)
    myDict = {}
    myDict["file1"] = fileName1Sentence
    myDict4 = []
    listFileName = {}
    myDict4 = makeData(len(internetPage), dataReadDoc, reportDataReadDoc)

    listFileName = internetPage
    myDict["ListFileName"] = listFileName
    myDict["File1Name"] = fileName1
    myDict["ListFile"] = myDict4

    return myDict


# kiểm vs internet
@api_view(('POST',))
def documentimportInternet(request):
    # fileName1 = request.data['fileName1']
    # userId = request.data['id']
    data1 = request.data
    myDict = test2(data1)
    return Response(myDict, status=status.HTTP_200_OK)


# import mới
# dùng kiểm với data ng dùng
@api_view(('POST', 'GET'))
def documentimport(request):
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
    # cursor = connections['default'].cursor()
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
        formatQuery('DocumentFile', os.path.basename(str(fetchQuery))))
    fileName1Sentence = lstSentence

    # fileName2
    # chạy preprocess cho từng file trong fileName2
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
                formatQuery('DocumentFile', os.path.basename(str(fetchQuery))))
            lst2 = lstSentence
            dataReadDoc.append(lst2)
        except Exception:
            pass

    # B2 trả json
    # result so sánh
    reportDataReadDoc = []
    for i in range(len(dataReadDoc)):
        result = ExportOrder(fileName1Sentence, dataReadDoc[i], rat)
        reportDataReadDoc.append(result)
    myDict = {}
    myDict4 = []
    listFileName = {}
    myDict4 = makeData(len(fileName2), dataReadDoc, reportDataReadDoc)

    # line length list
    listFileName = fileName2
    myDict["file1"] = fileName1Sentence
    myDict["ListFileName"] = listFileName
    myDict["ListFile"] = myDict4
    myDict["File1Name"] = fileName1
    return Response(myDict, status=status.HTTP_200_OK)


@api_view(('POST', 'GET'))
def FinalCheck(request):
    choice = request.data['choice']
    # filename = request.data['id']
    if choice is not None:
        print(choice)
        print(type(choice))
        if choice == 1:
            redirect('')
        elif choice == 2:
            print('database')
            res = documentimportDatabase()
            print('res is ------------------', res)
            return Response(res, status.HTTP_200_OK)
        elif choice == 3:
            print('internet')
            res = documentimportInternet(request.data)
            print('res is ------------------', res)
            return Response(res, status.HTTP_200_OK)
        elif choice == 4:
            res = documentimportDatabaseInternet(request.data)
            return Response(res, status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)


# upload 1 file
@api_view(('POST',))
def uploadDoc(request):
    content = None
    if request.method == 'POST':
        id = request.data["id"]
        form1 = UploadOneFileForm(request.POST, request.FILES)

        if form1.is_valid():

            # save form người dùng gửi
            data = form1.cleaned_data
            file1 = data['DataDocumentFile']  # abc.doc
            file_name = file1.name.split(".")[0]  # doc
            extension = file1.name.split(".")[-1]  # abc
            content = file_name
            data = DataDocument(
                DataDocumentName=file_name,
                DataDocumentAuthor_id=id,
                DataDocumentType=extension,
                DataDocumentFile=file1)
            data.save()
            # data= form1.save(commit = False)
            # agreeStatus = FileName if true, =0 if false
            agreeStatus = checkAgree(False, data=data)
            result = file_name + '.' + extension
            res = result
            content = {'filename': file1}
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response(content, status=status.HTTP_204_NO_CONTENT)

    else:
        # form = UploadOneFileForm()
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
        for f in listfile:
            # name = listname[count]
            count = count + 1
            file1: file
            file1 = f  # abc.doc
            file_name = file1.name.split(".")[0]  # doc
            extension = file1.name.split(".")[-1]  # abc
            filenameList.append(file1.name)

            data = DataDocument(
                DataDocumentName=file_name,
                DataDocumentAuthor_id=id,
                DataDocumentType=extension,
                DataDocumentFile=file1
                )
            data.save()
            agreeStatus = checkAgree(False, data=data)
        response = {'data': filenameList}
        return JsonResponse(response, status=status.HTTP_200_OK)
    else:
        # form = UploadManyFileForm()
        content = {'please move along': 'have the same username'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def test(self):
    content = {'please move along': 'have the same username222'}
    return Response(content, status=status.HTTP_200_OK)


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
        id = request.data["id"]
        form1 = UploadOneFileForm(request.POST, request.FILES)
        if form1.is_valid():

            # save form người dùng gửi
            data = form1.cleaned_data
            file1 = data['DataDocumentFile']  # abc.doc

            file_name = file1.name.split(".")[0]  # doc
            extension = file1.name.split(".")[-1]  # abc
            content = file_name
            data = DataDocument(
                DataDocumentName=file_name,
                DataDocumentAuthor_id=id,
                DataDocumentType=extension,
                DataDocumentFile=file1)
            data.save()
            # data= form1.save(commit = False)

            fName, lstSentence, lstLength = p.preprocess(
                formatString(
                    'DocumentFile',
                    data.DataDocumentName,
                    data.DataDocumentType))
            # //save to db//
            length = len(lstSentence)
            for i in range(length):
                data.datadocumentcontent_set.create(
                    DataDocumentSentence=lstSentence[i],
                    DataDocumentSentenceLength=lstLength[i]
                    )
            result = file_name + '.' + extension
            res = result
            content = {'filename': file1}
            return Response(res, status=status.HTTP_200_OK)
            # fake mocking
        else:
            # wrong form type
            return Response(content, status=status.HTTP_204_NO_CONTENT)
    else:
        # form = UploadOneFileForm()
        content = {'please move along': 'have the same username'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def ff(self):
    p.docx2txt("D:/project_doc.docx")


# upload multiple file vo luu tru cau db cua he thong(khac userdb)
def uploadMultipleDocumentSentenceToDatabase(request):
    content = None
    if request.method == 'POST':
        id = request.data["id"]
        listfile = request.FILES.getlist('DataDocumentFile')
        filenameList = []
        count = 0
        for f in listfile:
            # name = listname[count]
            count = count + 1
            file1: file
            file1 = f  # abc.doc
            file_name = file1.name.split(".")[0]  # doc
            extension = file1.name.split(".")[-1]  # abc
            filenameList.append(file1.name)

            data = DataDocument(
                DataDocumentName=file_name,
                DataDocumentAuthor_id=id,
                DataDocumentType=extension,
                DataDocumentFile=file1
                )
            data.save()

            fName, lstSentence, lstLength = p.preprocess(
                formatString(
                    'DocumentFile',
                    data.DataDocumentName,
                    data.DataDocumentType))
            # //save to db//
            length = len(lstSentence)
            for i in range(length):
                data.datadocumentcontent_set.create(
                    DataDocumentSentence=lstSentence[i],
                    DataDocumentSentenceLength=lstLength[i]
                    )

        response = {'data': filenameList}

        return JsonResponse(response, status=status.HTTP_200_OK)
    else:
        # form = UploadManyFileForm()
        content = {'please move along': 'have the same username'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


# up 1 file vao user db (chua xai)
# uploadDoc3 old -> uploadOneDocUser (change name only)
def jsonFile(request, file_name, userId):
    filename = "{root}/{folder}/{filename}{id}"
    filename.format(
        root=settings.MEDIA_ROOT,
        folder="result",
        filename=file_name,
        id=userId)
    # print("fullpath:          ", filename)
    mydict = request
    with open(filename + ".json", "w") as f:
        json.dump(mydict, f)
    fileJson = open(filename + ".json", "r")
    # reportData = json.loads(fileJson.read())
    # print(fileJson.name)
    fileJson.close()
    # os.remove(fileJson.name)
    return fileJson.name


# @api_view(['GET'])
# def test(self):
#     print('done')
#     content = {'please move along': 'have the same username222'}
#     return Response(content, status=status.HTTP_200_OK)

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
#     print("=======",fetchQuery," ",
#       str(userId)," ",
#       fileName1.split(".")[0]," ",
#       fileName1.split(".")[1])
#
#     # 1 internet link access theo user
#     internetTitle = "cau-6-trang-73-sgk-gdcd-11.jsp"
#     querys = DataDocumentT.objects.filter(DataDocumentType="internet")\
#         .filter(DataDocumentAuthor=str(userId))\
#         .filter(DataDocumentName=internetTitle)
#     # check all internet link
#     # querys = DataDocumentT.objects.filter(
#     #     DataDocumentType="internet"
#     #     ).filter(
#     #     DataDocumentName=internetTitle
#     #     )
#     fetchQuery =querys[0].DataDocumentFile
#     print("=======",fetchQuery," ",
#     str(userId)," ",
#     fileName1.split(".")[0]," ",
#     fileName1.split(".")[1])
#     # check file exist
#     print("======check=",querys.exists())
#
#     myDict={}
