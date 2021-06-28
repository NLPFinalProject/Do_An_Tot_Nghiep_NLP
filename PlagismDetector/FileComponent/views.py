import re
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.http import Http404
from rest_framework.response import Response
import json
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework import status
# cần import cho db
from .models import DataDocument, DataDocumentContent, DocumentSession, ReportDocument
from django.db import connections, connection
# can import cho levenshtein
from .levenshtein import ExportOrder
from PreprocessingComponent.views import *
# cần import cho up file
from django.core.files.storage import FileSystemStorage
from .form import UploadOneFileForm, UploadManyFileForm
from django.conf import settings
from PreprocessingComponent import views as p
from PreprocessingComponent import TFIDF as internetKeywordSearch
from UserComponent.models import User
import MailComponent.views as mail
# import cho tách câu
import os
from collections import Counter
from func_timeout import func_timeout, FunctionTimedOut
from UserComponent.models import User
import time
# import json

numPageSearch = 5
resultRatio = 50
maxFile = 1
rat = 50
timeout=6 # 6 seconds

# tinh trong exportorder cai phan tram lai
# them try catch owr cac ham inport va test, makedatareadoc.
# sua document status thanh 0,1,2


# format string
# folder = DocumentFile
# fileName = filename
# extension = extension
def formatString(folder, fileName, extension):
    FileString = "{base}\\{folder}\\{fileName}.{extension}".format(
        base=settings.MEDIA_ROOT,
        folder=folder,
        fileName=fileName,
        extension=extension)
    return FileString


# format query
# folder = DocumentFile
# fileName = filename
def formatQuery(folder, fileName):
    FileString = "{base}\\{folder}\\{fileName}".format(
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
                  "WHERE MATCH(DataDocumentSentence) AGAINST({sentence})".format(
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
    successlink = []
    for link in internetPage:
        try:
            if (internetKeywordSearch.is_downloadable(link)):
                # link_pdf.append(link)
                file_pdf = internetKeywordSearch.download_document(link)
                file_preprocessed = p.preprocess(file_pdf)
                data = DataDocument(
                    DataDocumentName=link,
                    DataDocumentAuthor_id=userId,
                    DataDocumentType="internetPdf",
                    DataDocumentFile=file_preprocessed[2]
                )
                data.save()
                dataReadDoc.append(file_preprocessed[0])
                successlink.append(link)
                print("\nlink này thành công:=====\n",link)
                for sentence in file_preprocessed[0]:
                    data.datadocumentcontent_set.create(
                        DataDocumentSentence=sentence,
                        DataDocumentSentenceLength=len(sentence))
                os.remove(file_pdf)
            else:
                try:
                    lstSentence = func_timeout(timeout, internetKeywordSearch.crawl_web(link))
                except FunctionTimedOut:
                    continue
                if lstSentence == None:
                    continue
                data = DataDocument(
                    DataDocumentName=link,
                    DataDocumentAuthor_id=userId,
                    DataDocumentType="internet",
                    DataDocumentFile=link
                )
                data.save()
                dataReadDoc.append(lstSentence)
                successlink.append(link)
                print("\nlink này thành công:=====\n",link)
                for sentence in lstSentence:
                    data.datadocumentcontent_set.create(
                        DataDocumentSentence=sentence,
                        DataDocumentSentenceLength=len(sentence))
            if(len(dataReadDoc) >= 5):
                break
        except:
            pass
    return dataReadDoc, successlink


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
    query = User.objects.get(pk=request.data['id'])
    if(query.is_lock==1):
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    data1 = request.data
    try:
        data1["filenameA"], session = uploadDoc2(
            request.POST, request.FILES, request.data['id'], request.data["agreeStatus"], request.data["sessionName"],
            "Database")
    except:
        session = DocumentSession(NumOfFile=1, SessionUser=id, Status="Fail")
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    myDict, fileName1, userId = test1(data1, session)
    if(myDict == None and fileName1==None and userId==None):
        session = DocumentSession(NumOfFile=1, SessionUser=id, Status="Fail")
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    jsonFile(myDict, fileName1, userId, session)
    jsonData = readJson(session, userId)
    session1 = DocumentSession.objects.get(pk=session)
    session1.Status = 'Success'
    session1.save()
    # mail.sendExportMailV2(request.data)
    sessionId = session1.id
    mail.sendExportMailV2(request.data, sessionId)
    return Response(status=status.HTTP_200_OK)


# kiểm vs internet
@api_view(('POST',))
def documentimportInternet(request):
    query = User.objects.get(pk=request.data['id'])
    if (query.is_lock == 1):
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    data1 = request.data

    try:
        data1["filenameA"], session = uploadDoc2(
            request.POST, request.FILES, request.data['id'], request.data["agreeStatus"], request.data["sessionName"],
            "Internet")
    except:
        session = DocumentSession(NumOfFile=1, SessionUser=id, Status="Fail")
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    myDict, fileName1, userId = test2(data1, session)
    jsonFile(myDict, fileName1, userId, session)
    jsonData = readJson(session, userId)
    session1 = DocumentSession.objects.get(pk=session)
    session1.Status = "Success"
    session1.save()
    sessionId = session1.id
    mail.sendExportMailV2(request.data, sessionId)
    # return Response(myDict, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)


@api_view(('POST',))
def documentimportDatabaseInternet(request):
    query = User.objects.get(pk=request.data['id'])
    if (query.is_lock == 1):
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    data1 = request.data
    try:
        data1["filenameA"], session = uploadDoc2(
            request.POST, request.FILES, request.data['id'], request.data["agreeStatus"], request.data["sessionName"],
            "Database and internet")
    except:
        session = DocumentSession(NumOfFile=1, SessionUser=id, Status="Fail")
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    # try catch status here here
    try:
        myDict1, fileName1, userId = test1(data1, session)
        myDict2, fileName1, userId = test2(data1, session)
        myDict1["AllFileRatio"].extend(myDict2["AllFileRatio"])
        myDict2["ListAllFile"].pop(0)
        myDict1["ListAllFile"].extend(myDict2["ListAllFile"])
        myDict1["ListFileName"].extend(myDict2["ListFileName"])
        myDict1["ListFile"].extend(myDict2["ListFile"])

        jsonFile(myDict1, fileName1, userId, session)
        # myDict1 = test1(data1)
        # EmyDict2 = test2(data1)

        jsonData = readJson(session, userId)
        session1 = DocumentSession.objects.get(pk=session)
        session1.Status = 'Success'
        # session1.Status = "Thành công"
        session1.save()
        sessionId = session1.id
        mail.sendExportMailV2(request.data, sessionId)
        return Response(status=status.HTTP_200_OK)
    except:
        session1 = DocumentSession.objects.get(pk=session)
        # session1.Status = False "Thất bại"
        session1.save()
        sessionId = session1.id
        mail.sendExportMailV2(request.data, sessionId)
        return Response(status=status.HTTP_200_OK)


# import mới
# dùng kiểm với data ng dùng
@api_view(('POST', 'GET'))
def documentimport(request):
    query = User.objects.get(pk=request.data['id'])
    if(query.is_lock==1):
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    data1 = request.data
    try:
        data1["filenameA"], session = uploadDoc2(
            request.POST, request.FILES, request.data['id'], request.data["agreeStatus"], request.data["sessionName"],
            "Multiple files")
    except:
        session = DocumentSession(NumOfFile=1, SessionUser=id, Status="Fail")
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    data1["filenameB"] = uploadDocList2(
        request.POST, request.FILES, request.data['id'], session, request.data["agreeStatus"])

    myDict, fileName1, userId = test3(data1, session)
    jsonFile(myDict, fileName1, userId, session)
    jsonData = readJson(session, userId)
    session1 = DocumentSession.objects.get(pk=session)
    if(session1.ChildReport > 0):
        session1.Status = 'Success'
    else:
        session1.Status = "Fail"
    session1.save()
    sessionId = session1.id
    mail.sendExportMailV2(request.data, sessionId)
    return Response(status=status.HTTP_200_OK)


# hệ thống
def test1(data, session):
    fileName1 = data["filenameA"]
    userId = int(data["id"])
    fileName2Sentence = []
    # cursor = connections['default'].cursor()
    # fileName1
    querys = DataDocument.objects \
        .filter(DataDocumentAuthor=str(userId)) \
        .filter(DataDocumentName=fileName1.split(".")[0]) \
        .filter(DataDocumentType=fileName1.split(".")[1]) \
        .filter(SessionId=session)
    fetchQuery = querys[0].DataDocumentFile
    try:
        file_preprocessed = p.preprocess(
            formatQuery('DocumentFile', os.path.basename(str(fetchQuery))))
        fileName1Sentence = file_preprocessed[0]
    except:
        return -1, -1, -1

    # database search
    documentName = databaseSearch(fileName1Sentence)

    # thong ke
    idStatistic = Counter(documentName)
    countReport = 0
    reportDataReadDoc = []
    ReportFileName2Sentence = []
    reportIdFile = []
    fileName2 = []
    fileRatio = []
    for idFile in idStatistic.items():
        if (countReport < maxFile):
            querys = DataDocumentContent.objects.filter(
                DataDocumentNo_id=int(idFile[0])).order_by('id')
            fileName2Sentence = [
                querys[i].DataDocumentSentence for i in range(len(querys))]
            result = ExportOrder(
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
                fileRatio.append(result[1])

    myDict = {}
    myDict["AllFileRatio"] = fileRatio
    myDict["ListAllFile"] = []
    myDict["ListAllFile"].append(fileName1)
    myDict["File1Name"] = fileName1
    myDict4 = makeData(countReport, ReportFileName2Sentence, reportDataReadDoc)

    # line length list
    myDict["ListFileName"] = fileName2
    myDict["ListFile"] = myDict4
    myDict["file1"] = fileName1Sentence
    querys = DataDocument.objects \
        .filter(DataDocumentAuthor=str(userId)) \
        .filter(DataDocumentName=fileName1.split(".")[0]) \
        .filter(DataDocumentType=fileName1.split(".")[1]) \
        .filter(SessionId=session)
    resfileid = querys[0].id
    resfile = DataDocument.objects.get(pk=resfileid)
    resfile.DocumentStatus = True
    resfile.save()
    return myDict, fileName1, userId


def test2(data, session):
    fileName1 = data['filenameA']
    userId = int(data['id'])
    # cursor = connections['default'].cursor()
    # fileName1
    querys = DataDocument.objects \
        .filter(DataDocumentAuthor=str(userId)) \
        .filter(DataDocumentName=fileName1.split(".")[0]) \
        .filter(DataDocumentType=fileName1.split(".")[1]) \
        .filter(SessionId=session)
    fetchQuery = querys[0].DataDocumentFile
    # return tag preprocess
    try:
        file_preprocessed = p.preprocess(
            formatQuery('DocumentFile', os.path.basename(str(fetchQuery))))
        fileName1Sentence = file_preprocessed[0]
    except:
        return None, None, None

    # internet search
    internetPage = internetKeywordSearch.get_link(file_preprocessed[0],file_preprocessed[1])
    print("link tìm được là: ", internetPage)
    dataReadDoc, sucessLink = makeDataReadDoc(internetPage, userId)
    # B2 trả json
    reportDataReadDoc = []
    fileRatio = []
    for i in range(len(dataReadDoc)):
        result = ExportOrder(fileName1Sentence, dataReadDoc[i], rat)
        reportDataReadDoc.append(result[0])
        fileRatio.append(result[1])
    myDict = {}
    myDict["file1"] = fileName1Sentence
    myDict["AllFileRatio"] = fileRatio
    myDict["ListAllFile"] = []
    myDict["ListAllFile"].append(fileName1)
    myDict["ListAllFile"].extend(sucessLink)

    myDict4 = makeData(len(sucessLink), dataReadDoc, reportDataReadDoc)

    listFileName = sucessLink
    myDict["ListFileName"] = listFileName
    myDict["File1Name"] = fileName1
    myDict["ListFile"] = myDict4
    querys = DataDocument.objects \
        .filter(DataDocumentAuthor=str(userId)) \
        .filter(DataDocumentName=fileName1.split(".")[0]) \
        .filter(DataDocumentType=fileName1.split(".")[1]) \
        .filter(SessionId=session)
    resfileid = querys[0].id
    resfile = DataDocument.objects.get(pk=resfileid)
    resfile.DocumentStatus = True
    resfile.save()
    return myDict, fileName1, userId


def test3(data, session):
    fileName1 = data["filenameA"]
    userId = int(data['id'])
    fileName2 = data["filenameB"]
    # if request.method == 'POST':
    #     fileName1 = request.data["filename1"]
    #     fileName2 = request.data["listfile"]
    #     userId = int(request.data["id"])
    # elif request.method == 'GET':
    #     fileName1 = request.GET.get["filename1"]
    #     fileName2 = request.GET.get["listfile"]
    #     userId = int(request.GET.get["id"])
    # cursor = connections['default'].cursor()
    # B1 start đọc data từ database
    # fileName1
    # query trên database
    querys = DataDocument.objects \
        .filter(DataDocumentAuthor=str(userId)) \
        .filter(DataDocumentName=fileName1.split(".")[0]) \
        .filter(DataDocumentType=fileName1.split(".")[1]) \
        .filter(SessionId=session)
    fetchQuery = querys[0].DataDocumentFile
    try:
        file_preprocessed = p.preprocess(
            formatQuery('DocumentFile', os.path.basename(str(fetchQuery))))
        fileName1Sentence = file_preprocessed[0]
    except:
        return -1, -1, -1

    # fileName2
    # chạy preprocess cho từng file trong fileName2
    dataReadDoc = []
    successFile = []
    for fileUName in fileName2:
        try:
            # query database
            querys = DataDocument.objects.filter(
                DataDocumentAuthor=str(userId)) \
                .filter(DataDocumentName=fileUName.split(".")[0]) \
                .filter(DataDocumentType=fileUName.split(".")[1]) \
                .filter(SessionId=session)
            fetchQuery = querys[0].DataDocumentFile
            file_preprocessed = p.preprocess(
                formatQuery('DocumentFile', os.path.basename(str(fetchQuery))))
            lst2 = file_preprocessed[0]
            dataReadDoc.append(lst2)
            successFile.append(fileUName)
            a = DocumentSession.objects.get(pk=session)
            a.ChildReport = a.ChildReport + 1
            a.save()
        except Exception:
            if(len(fileName2)==1):
                a = DocumentSession.objects.get(pk=session)
                a.Status="Fail"
                a.save()
            pass
    fileName2 = successFile
    # B2 trả json
    # result so sánh
    reportDataReadDoc = []
    fileRatio = []
    for i in range(len(dataReadDoc)):
        result = ExportOrder(fileName1Sentence, dataReadDoc[i], rat)
        reportDataReadDoc.append(result[0])
        fileRatio.append(result[1])
    myDict = {}
    myDict4 = makeData(len(fileName2), dataReadDoc, reportDataReadDoc)
    # line length list
    listFileName = fileName2
    myDict["file1"] = fileName1Sentence
    myDict["ListFileName"] = listFileName
    myDict["ListFile"] = myDict4
    myDict["File1Name"] = fileName1
    myDict["AllFileRatio"] = fileRatio
    myDict["ListAllFile"] = []
    myDict["ListAllFile"].append(fileName1)
    myDict["ListAllFile"].extend(fileName2)
    querys = DataDocument.objects \
        .filter(DataDocumentAuthor=str(userId)) \
        .filter(DataDocumentName=fileName1.split(".")[0]) \
        .filter(DataDocumentType=fileName1.split(".")[1]) \
        .filter(SessionId=session)
    resfileid = querys[0].id
    resfile = DataDocument.objects.get(pk=resfileid)
    resfile.DocumentStatus = True
    resfile.save()
    return myDict, fileName1, userId


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


def uploadDoc2(PostData, FileData, ID, agreeStatus, sessionName, sessionType):
    content = None

    id = ID
    form1 = UploadOneFileForm(PostData, FileData)

    if form1.is_valid():
        # save form người dùng gửi
        data = form1.cleaned_data
        file1 = data['DataDocumentFile']  # abc.doc
        file_name = file1.name.split(".")[0]  # doc
        extension = file1.name.split(".")[-1]  # abc
        content = file_name
        session = DocumentSession(NumOfFile=1, SessionUser=id, SessionName=sessionName, SessionType=sessionType)
        session.save()
        data = DataDocument(
            DataDocumentName=file_name,
            DataDocumentAuthor_id=id,
            DataDocumentType=extension,
            DataDocumentFile=file1,
            SessionId=session.id,
        )

        data.save()

        # data= form1.save(commit = False)
        # agreeStatus = FileName if true, =0 if false
        if (agreeStatus):

            file_preprocessed = p.preprocess(
                formatString(
                    'DocumentFile',
                    data.DataDocumentName,
                    data.DataDocumentType))

            # //save to db//
            length = len(file_preprocessed[0])
            for i in range(length):
                a = data.datadocumentcontent_set.create(
                    DataDocumentSentence=file_preprocessed[0][i],
                    DataDocumentSentenceLength=len(file_preprocessed[0][i]))
        result = file_name + '.' + extension
        content = {'filename': file1}
        return result, session.id


@api_view(('POST',))
def uploadDocListRequest(request):
    # chuong trinh test
    content = None
    PostData = request.POST
    FileData = request.FILES
    ID = request.data['id']

    id = ID
    listfile = FileData.getlist('DataDocumentFileList')
    filenameList = []
    count = 0
    # session = DocumentSession.objects.get(pk=session)
    # session.NumOfFile = 1 + len(listfile)
    # session.save()
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

        file_preprocessed = p.preprocess(
            formatString(
                'DocumentFile',
                data.DataDocumentName,
                data.DataDocumentType))
        # //save to db//
        length = len(file_preprocessed[0])
        for i in range(length):
            data.datadocumentcontent_set.create(
                DataDocumentSentence=file_preprocessed[0][i],
                DataDocumentSentenceLength=len(file_preprocessed[0][i]))
    response = {'data': filenameList}
    return Response(response, status=status.HTTP_200_OK)


def uploadDocList2(PostData, FileData, ID, session, agreeStatus):
    # chuong trinh test
    content = None

    id = ID
    listfile = FileData.getlist('DataDocumentFileList')
    filenameList = []
    count = 0
    session = DocumentSession.objects.get(pk=session)
    session.NumOfFile = 1 + len(listfile)
    session.save()
    for f in listfile:
        try:
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
                DataDocumentFile=file1,
                SessionId=session.id
            )
            data.save()
            if (agreeStatus):
                file_preprocessed = p.preprocess(
                    formatString(
                        'DocumentFile',
                        data.DataDocumentName,
                        data.DataDocumentType))
                # //save to db//
                length = len(file_preprocessed[0])
                for i in range(length):
                    data.datadocumentcontent_set.create(
                        DataDocumentSentence=file_preprocessed[0][i],
                        DataDocumentSentenceLength=len(file_preprocessed[0][i]))
        except:
            pass
    response = {'data': filenameList}
    return filenameList


#     return JsonResponse(response, status=status.HTTP_200_OK)
# else:
#     # form = UploadManyFileForm()
#     content = {'please move along': 'have the same username'}
#     return Response(content, status=status.HTTP_204_NO_CONTENT)

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

            file_preprocessed = p.preprocess(
                formatString(
                    'DocumentFile',
                    data.DataDocumentName,
                    data.DataDocumentType))
            # //save to db//
            length = len(file_preprocessed[0])
            for i in range(length):
                data.datadocumentcontent_set.create(
                    DataDocumentSentence=file_preprocessed[0][i],
                    DataDocumentSentenceLength=len(file_preprocessed[0][i]))
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

            file_preprocessed = p.preprocess(
                formatString(
                    'DocumentFile',
                    data.DataDocumentName,
                    data.DataDocumentType))
            # //save to db//
            length = len(file_preprocessed[0])
            for i in range(length):
                data.datadocumentcontent_set.create(
                    DataDocumentSentence=file_preprocessed[0][i],
                    DataDocumentSentenceLength=len(file_preprocessed[0][i])
                )

        response = {'data': filenameList}

        return JsonResponse(response, status=status.HTTP_200_OK)
    else:
        # form = UploadManyFileForm()
        content = {'please move along': 'have the same username'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


# up 1 file vao user db (chua xai)
# uploadDoc3 old -> uploadOneDocUser (change name only)
def jsonFile(request, file_name, userId, session):
    filename = "{root}/{folder}/{session}{filename}{id}.json".format(
        root=settings.MEDIA_ROOT,
        folder="result",
        filename=file_name,
        id=userId,
        session=session)
    # print("fullpath:          ", filename)
    mydict = request
    with open(filename, "w") as f:
        json.dump(mydict, f)

    temp = DataDocument.objects.filter(DataDocumentAuthor=str(userId)) \
        .filter(DataDocumentName=file_name.split(".")[0]) \
        .filter(SessionId=str(session)) \
        .filter(DocumentStatus=True)

    idFile = temp[0].id
    data = ReportDocument(DocumentJson_id=int(idFile),
                          JsonFile=filename)

    data.save()
    # fileJson = open(filename, "r")
    # reportData = json.loads(fileJson.read()) - 0<50
    # print(fileJson.name)-20>10
    # fileJson.close()
    # os.remove(fileJson.name)
    # return fileJson.name


def readJson(session, userId):
    temp = DataDocument.objects.filter(DataDocumentAuthor=str(userId)) \
        .filter(SessionId=str(session)) \
        .filter(DocumentStatus=True)
    idFile = temp[0].id
    data = ReportDocument.objects.get(DocumentJson_id=idFile)
    fileJson = open(data.JsonFile, "r")
    reportData = json.loads(fileJson.read())
    fileJson.close()
    # os.remove(fileJson.name)

    return reportData


@api_view(('GET', 'POST'))
def readJsonRequest(request):
    if request.method == 'POST':
        try:
            #print(request.data['id'])
            #print(request.data["sessionId"])
            session = request.data['sessionId']
            userId = request.data['id']
            temp = DataDocument.objects.filter(DataDocumentAuthor=str(userId)) \
                .filter(SessionId=str(session)) \
                .filter(DocumentStatus=True)
            idFile = temp[0].id
            data = ReportDocument.objects.get(DocumentJson_id=idFile)
            fileJson = open(data.JsonFile, "r")
            reportData = json.loads(fileJson.read())
            fileJson.close()
            # os.remove(fileJson.name)
            print("report data là: ", reportData)

            return Response(reportData, status=status.HTTP_200_OK)
        except:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        print("what are thou")
        print(request.GET)
        session = request.GET['sessionId']
        userId = request.GET['id']
        temp = DataDocument.objects.filter(DataDocumentAuthor=str(userId)) \
            .filter(SessionId=str(session)) \
            .filter(DocumentStatus=True)
        idFile = temp[0].id
        data = ReportDocument.objects.get(DocumentJson_id=idFile)
        fileJson = open(data.JsonFile, "r")
        reportData = json.loads(fileJson.read())
        fileJson.close()
        # os.remove(fileJson.name)
        print("report data là: ", reportData)
        return Response(reportData, status=status.HTTP_200_OK)







