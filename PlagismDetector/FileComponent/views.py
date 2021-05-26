# from rest_framework.decorators import api_view
# from django.shortcuts import render, redirect
# from django.http import Http404
# from rest_framework.response import Response
# import json
# from django.http.response import JsonResponse
# from django.http import HttpResponse
# from rest_framework import status
# # cần import cho db
# from .models import *
# from django.db import connections, connection
# # can import cho levenshtein
# from .levenshtein import *
# from PreprocessingComponent.views import *
# # cần import cho up file
# from django.core.files.storage import FileSystemStorage
# # lock command UploadOneFileForm lại trước khi migrations vì sửa dụng model DocumentFile
# # from .form import DocumentForm, UploadOneFileForm, UploadManyFileForm
# from .form import UploadOneFileForm, UploadManyFileForm
# from django.conf import settings
# from PreprocessingComponent import views as p
# from PreprocessingComponent import TFIDF as internetKeywordSearch
# # import cho tách câu
# import os
# from collections import Counter
# import json
# import time

# numPageSearch = 5
# resultRatio = 50
# maxFile = 1
# rat = 50


# # database search
# def databaseSearch(fileName1Sentence):
#     documentName = []
#     documentNameId = []
#     cursor = connections['default'].cursor()
#     for fileSentence in fileName1Sentence:
#         sentence = chr(34) + fileSentence.replace(chr(34), "") + chr(34)
#         queryRaw = "SELECT id FROM `filecomponent_datadocumentcontent` WHERE MATCH(DataDocumentSentence) AGAINST(" + \
#             sentence + ")"
#         cursor.execute(queryRaw)
#         fetchQuery = dictfetchall(cursor)
#         documentNameFind = [a_dict["id"] for a_dict in fetchQuery]
#         documentNameId.extend(documentNameFind)
#     documentNameId = list(dict.fromkeys(documentNameId))

#     for idDoc in documentNameId:
#         querys = DataDocumentContent.objects.filter(id=str(idDoc))
#         querys = DataDocument.objects.filter(id=querys[0].DataDocumentNo_id)
#         documentName.append(str(querys[0].id))
#     return documentName

# def makeDataReadDoc(internetPage,userId):
#     dataReadDoc = []
#     for link in internetPage:
#         if (internetKeywordSearch.is_downloadable(link)):
#             # link_pdf.append(link)
#             file_pdf = internetKeywordSearch.download_document(link)
#             fName, lstSentence, lstLength = p.preprocess(file_pdf)
#             data = DataDocument(
#                 DataDocumentName=os.path.basename(file_pdf),
#                 DataDocumentAuthor_id=userId,
#                 DataDocumentType="internetPdf",
#                 DataDocumentFile=link
#                 )
#             data.save()
#             dataReadDoc.append(lstSentence)
#             # length= len(lstSentence)
#             # for i in range(length):
#             #     c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])

#             # os.remove(file_pdf)
#         else:
#             fName = os.path.basename(link)
#             lstSentence = internetKeywordSearch.crawl_web(link)
#             data = DataDocument(
#                 DataDocumentName=link,
#                 DataDocumentAuthor_id=userId,
#                 DataDocumentType="internet",
#                 DataDocumentFile=link
#                 )
#             data.save()
#             dataReadDoc.append(lstSentence)
#             # length= len(lstSentence)
#             # for i in range(length):
#             #     c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=len(lstSentence[i]))
#     return dataReadDoc

# def makeDataStt(countReport,ReportFileName2Sentence,reportDataReadDoc):
#     myDict4 = []
#     for i in range(countReport):
#         mydic3 = {}
#         mydic3["data"] = ReportFileName2Sentence[i]
#         mydic3["stt"] = reportDataReadDoc[i]
#         myDict4.append(mydic3)
#     return myDict4


# # result
# # systemSearch
# @api_view(('POST',))
# def documentimportDatabase(request):
#     fileName1 = request.data["filename1"]
#     userId = int(request.data["id"])
#     data1 = request.data
#     myDict=test1(data1)
#     return Response(myDict, status=status.HTTP_200_OK)
#     # fileName2Sentence = []
#     # cursor = connections['default'].cursor()
#     # # fileName1
#     # querys = DataDocument.objects.filter(
#     #     DataDocumentAuthor=str(userId)) \
#     #     .filter(DataDocumentName=fileName1.split(".")[0]) \
#     #     .filter(DataDocumentType=fileName1.split(".")[1])
#     # fetchQuery = querys[0].DataDocumentFile
#     # fName, lstSentence, lstLength = p.preprocess(
#     #     settings.MEDIA_ROOT + '/DocumentFile/' + os.path.basename(str(fetchQuery)))
#     # fileName1Sentence = lstSentence
#     #
#     # # database search
#     # documentName = databaseSearch(fileName1Sentence)
#     #
#     # # thong ke
#     # idStatistic = Counter(documentName)
#     # countReport = 0
#     # reportDataReadDoc = []
#     # ReportFileName2Sentence = []
#     # reportIdFile = []
#     # fileName2 = []
#     # for idFile in idStatistic.items():
#     #     if (countReport < maxFile):
#     #         querys = DataDocumentContent.objects.filter(
#     #             DataDocumentNo_id=int(idFile[0])).order_by('id')
#     #         fileName2Sentence = [
#     #             querys[i].DataDocumentSentence for i in range(len(querys))]
#     #         result = ExportOrder4(
#     #             fileName1Sentence, fileName2Sentence, resultRatio)
#     #         if (result[1] >= resultRatio and countReport < maxFile):
#     #             countReport += 1
#     #             reportIdFile.append(idFile[0])
#     #             reportDataReadDoc.append(result[0])
#     #             ReportFileName2Sentence.append(fileName2Sentence)
#     #             # querys = DataDocument.objects.filter(id=str(idFile[0]))
#     #             # fileName2Name = querys[0].DataDocumentName
#     #             fileName2Name = str(querys[0].DataDocumentNo)
#     #             fileName2.append(fileName2Name)
#     #
#     # myDict4 = []
#     # myDict = {}
#     # myDict["File1Name"] = fileName1
#     # myDict4 = makeDataStt(countReport, ReportFileName2Sentence, reportDataReadDoc)
#     # # for i in range(countReport):
#     # #     mydic3 = {}
#     # #     mydic3["data"] = ReportFileName2Sentence[i]
#     # #     mydic3["stt"] = reportDataReadDoc[i]
#     # #     myDict4.append(mydic3)
#     #
#     # # line length list
#     # myDict["ListFileName"] = fileName2
#     # myDict["ListFile"] = myDict4
#     # myDict["file1"] = fileName1Sentence
#     # return Response(myDict, status=status.HTTP_200_OK)


# @api_view(('POST',))
# def documentimportDatabaseInternet(request):
#     fileName1 = request.data["fileName1"]
#     userId = int(request.data["id"])
#     data1 = request.data
#     myDict1 = test1(data1)
#     myDict2 = test2(data1)
#     myDict=[]
#     myDict.append(myDict1)
#     myDict.append(myDict2)
#     return Response(myDict, status=status.HTTP_200_OK)
#     # print("filename1: ",fileName1, userId)
#     # fileName2Sentence = []
#     # # fileName1
#     # querys = DataDocument.objects.filter(
#     #     DataDocumentAuthor=str(userId)) \
#     #     .filter(DataDocumentName=fileName1.split(".")[0]) \
#     #     .filter(DataDocumentType=fileName1.split(".")[1])
#     # fetchQuery = querys[0].DataDocumentFile
#     # # return tag preprocess
#     # tagPage, fName, lstSentence, lstLength = p.preprocess_link(
#     #     settings.MEDIA_ROOT + '/DocumentFile/' + os.path.basename(str(fetchQuery)))
#     # # internet search
#     # internetPage = internetKeywordSearch.get_link(
#     #     tagPage, fName, lstSentence, lstLength)
#     # if (len(internetPage) > numPageSearch):
#     #     internetPage = internetPage[:numPageSearch]
#     # fileName1Sentence = lstSentence
#     # # database search
#     # documentName = []
#     # documentName = databaseSearch(fileName1Sentence)
#     #
#     # # thong ke
#     # idStatistic = Counter(documentName)
#     # countReport = 0
#     # reportDataReadDoc = []
#     # ReportFileName2Sentence = []
#     # reportIdFile = []
#     # fileName2 = []
#     # for idFile in idStatistic.items():
#     #     if (countReport < maxFile):
#     #         querys = DataDocumentContent.objects.filter(
#     #             DataDocumentNo_id=int(idFile[0])).order_by('id')
#     #         fileName2Sentence = [
#     #             querys[i].DataDocumentSentence for i in range(len(querys))]
#     #         result = ExportOrder4(
#     #             fileName1Sentence, fileName2Sentence, resultRatio)
#     #         if (result[1] >= resultRatio and countReport < maxFile):
#     #             countReport += 1
#     #             reportIdFile.append(idFile[0])
#     #             reportDataReadDoc.append(result[0])
#     #             ReportFileName2Sentence.append(fileName2Sentence)
#     #             fileName2Name = str(querys[0].DataDocumentNo)
#     #             fileName2.append(fileName2Name)
#     #
#     # myDict4 = []
#     # myDict = {}
#     # myDict["File1Name"] = fileName1
#     # myDict4 = makeDataStt(countReport,ReportFileName2Sentence,reportDataReadDoc)
#     #
#     # # report cac cau html
#     # dataReadDoc = []
#     # dataReadDoc = makeDataReadDoc(internetPage,userId)
#     # # B2 trả json
#     # reportDataReadDoc = []
#     # for i in range(len(dataReadDoc)):
#     #     result = ExportOrder(fileName1Sentence, dataReadDoc[i], rat)
#     #     reportDataReadDoc.append(result)
#     # myDictHtml2 = []
#     # myDictHtml2 = makeDataStt(len(internetPage),dataReadDoc,reportDataReadDoc)
#     # fileName2.extend(internetPage)
#     #
#     # # line length list
#     # myDict["ListFileName"] = fileName2
#     # myDict["ListFile"] = myDict4
#     # myDict["file1"] = fileName1Sentence
#     # myDict["ListFile"].extend(myDictHtml2)
#     # myDict["internet"] = myDictHtml2
#     # return Response(myDict, status=status.HTTP_200_OK)

# def test1(data):
#     fileName1 = data["filename1"]
#     userId = int(data["id"])
#     fileName2Sentence = []
#     cursor = connections['default'].cursor()
#     # fileName1
#     querys = DataDocument.objects.filter(
#         DataDocumentAuthor=str(userId)) \
#         .filter(DataDocumentName=fileName1.split(".")[0]) \
#         .filter(DataDocumentType=fileName1.split(".")[1])
#     fetchQuery = querys[0].DataDocumentFile
#     fName, lstSentence, lstLength = p.preprocess(
#         settings.MEDIA_ROOT + '/DocumentFile/' + os.path.basename(str(fetchQuery)))
#     fileName1Sentence = lstSentence

#     # database search
#     documentName = databaseSearch(fileName1Sentence)

#     # thong ke
#     idStatistic = Counter(documentName)
#     countReport = 0
#     reportDataReadDoc = []
#     ReportFileName2Sentence = []
#     reportIdFile = []
#     fileName2 = []
#     for idFile in idStatistic.items():
#         if (countReport < maxFile):
#             querys = DataDocumentContent.objects.filter(
#                 DataDocumentNo_id=int(idFile[0])).order_by('id')
#             fileName2Sentence = [
#                 querys[i].DataDocumentSentence for i in range(len(querys))]
#             result = ExportOrder4(
#                 fileName1Sentence, fileName2Sentence, resultRatio)
#             if (result[1] >= resultRatio and countReport < maxFile):
#                 countReport += 1
#                 reportIdFile.append(idFile[0])
#                 reportDataReadDoc.append(result[0])
#                 ReportFileName2Sentence.append(fileName2Sentence)
#                 # querys = DataDocument.objects.filter(id=str(idFile[0]))
#                 # fileName2Name = querys[0].DataDocumentName
#                 fileName2Name = str(querys[0].DataDocumentNo)
#                 fileName2.append(fileName2Name)

#     myDict4 = []
#     myDict = {}
#     myDict["File1Name"] = fileName1
#     myDict4 = makeDataStt(countReport,ReportFileName2Sentence,reportDataReadDoc)
#     # for i in range(countReport):
#     #     mydic3 = {}
#     #     mydic3["data"] = ReportFileName2Sentence[i]
#     #     mydic3["stt"] = reportDataReadDoc[i]
#     #     myDict4.append(mydic3)

#     # line length list
#     myDict["ListFileName"] = fileName2
#     myDict["ListFile"] = myDict4
#     myDict["file1"] = fileName1Sentence

#     return myDict


# def test2(data):
#     fileName1 = data['fileName1']
#     userId = data['id']
#     cursor = connections['default'].cursor()
#     # fileName1
#     querys = DataDocument.objects.filter(
#         DataDocumentAuthor=str(userId)) \
#         .filter(DataDocumentName=fileName1.split(".")[0]) \
#         .filter(DataDocumentType=fileName1.split(".")[1])
#     fetchQuery = querys[0].DataDocumentFile
#     # return tag preprocess
#     tagPage, fName, lstSentence, lstLength = p.preprocess_link(
#         settings.MEDIA_ROOT + '/DocumentFile/' + os.path.basename(str(fetchQuery)))
#     fileName1Sentence = lstSentence

#     # internet search
#     internetPage = internetKeywordSearch.get_link(
#         tagPage, fName, lstSentence, lstLength)
#     if (len(internetPage) > numPageSearch):
#         internetPage = internetPage[:numPageSearch]
#     print("Link: ", internetPage)
#     dataReadDoc = makeDataReadDoc(internetPage,userId)

#     # B2 trả json
#     reportDataReadDoc = []
#     for i in range(len(dataReadDoc)):
#         # print("tao report ", i)
#         # start_time = time.time()
#         result = ExportOrder(fileName1Sentence, dataReadDoc[i], rat)
#         reportDataReadDoc.append(result)
#         # print("---tao report ", i, " nay mất %s seconds ---" %
#         #       (time.time() - start_time))

#     myDict = {}
#     myDict["file1"] = fileName1Sentence
#     myDict4 = []
#     listFileName = {}
#     myDict4 = makeDataStt(len(internetPage),dataReadDoc,reportDataReadDoc)

#     listFileName = internetPage
#     myDict["ListFileName"] = listFileName
#     myDict["File1Name"] = fileName1
#     myDict["ListFile"] = myDict4

#     # FileDatabase=DataDocument.objects.filter(DataDocumentName=fileName1.split(".")[0],DataDocumentType=fileName1.split(".")[1],DataDocumentAuthor_id=str(userId))
#     # jsonResult=ReportDocument(DataDocumentName=FileDatabase.,DataDocumentReport=RjsonFile(myDict,fileName1.split(".")[0],userId))
#     #jsonResult = jsonFile(myDict, fileName1.split(".")[0], userId)

#     return myDict


# # kiểm vs internet
# @api_view(('POST',))
# def documentimportInternet(request):
#     fileName1 = request.data['fileName1']
#     userId = request.data['id']
#     data1 = request.data
#     myDict = test2(data1)
#     return Response(myDict, status=status.HTTP_200_OK)

#     # cursor = connections['default'].cursor()
#     # # fileName1
#     # querys = DataDocument.objects.filter(
#     #     DataDocumentAuthor=str(userId)) \
#     #     .filter(DataDocumentName=fileName1.split(".")[0]) \
#     #     .filter(DataDocumentType=fileName1.split(".")[1])
#     # fetchQuery = querys[0].DataDocumentFile
#     # # return tag preprocess
#     # tagPage, fName, lstSentence, lstLength = p.preprocess_link(
#     #     settings.MEDIA_ROOT + '/DocumentFile/' + os.path.basename(str(fetchQuery)))
#     # fileName1Sentence = lstSentence
#     #
#     # # internet search
#     # internetPage = internetKeywordSearch.get_link(
#     #     tagPage, fName, lstSentence, lstLength)
#     # if (len(internetPage) > numPageSearch):
#     #     internetPage = internetPage[:numPageSearch]
#     # print("Link: ", internetPage)
#     # dataReadDoc = makeDataReadDoc(internetPage,userId)
#     #
#     # # B2 trả json
#     # reportDataReadDoc = []
#     # for i in range(len(dataReadDoc)):
#     #     # print("tao report ", i)
#     #     # start_time = time.time()
#     #     result = ExportOrder(fileName1Sentence, dataReadDoc[i], rat)
#     #     reportDataReadDoc.append(result)
#     #     # print("---tao report ", i, " nay mất %s seconds ---" %
#     #     #       (time.time() - start_time))
#     #
#     # myDict = {}
#     # myDict["file1"] = fileName1Sentence
#     # myDict4 = []
#     # listFileName = {}
#     # myDict4 = makeDataStt(len(internetPage),dataReadDoc,reportDataReadDoc)
#     #
#     # listFileName = internetPage
#     # myDict["ListFileName"] = listFileName
#     # myDict["File1Name"] = fileName1
#     # myDict["ListFile"] = myDict4
#     #
#     # # FileDatabase=DataDocument.objects.filter(DataDocumentName=fileName1.split(".")[0],DataDocumentType=fileName1.split(".")[1],DataDocumentAuthor_id=str(userId))
#     # # jsonResult=ReportDocument(DataDocumentName=FileDatabase.,DataDocumentReport=RjsonFile(myDict,fileName1.split(".")[0],userId))
#     # #jsonResult = jsonFile(myDict, fileName1.split(".")[0], userId)
#     # return Response(myDict, status=status.HTTP_200_OK)


# # import mới
# # dùng kiểm với data ng dùng
# @api_view(('POST', 'GET'))
# def documentimport(request):
#     fileName1 = None
#     fileName2 = None
#     userId = None
#     if request.method == 'POST':

#         fileName1 = request.data["filename1"]
#         fileName2 = request.data["listfile"]
#         userId = int(request.data["id"])
#     elif request.method == 'GET':
#         fileName1 = request.GET.get["filename1"]
#         fileName2 = request.GET.get["listfile"]
#         userId = int(request.GET.get["id"])
#     cursor = connections['default'].cursor()
#     # B1 start đọc data từ database
#     # fileName1
#     # query trên database
#     querys = DataDocument.objects.filter(
#         DataDocumentAuthor=str(userId)) \
#         .filter(DataDocumentName=fileName1.split(".")[0]) \
#         .filter(DataDocumentType=fileName1.split(".")[1]
#                 )
#     fetchQuery = querys[0].DataDocumentFile
#     fName, lstSentence, lstLength = p.preprocess(
#         settings.MEDIA_ROOT + '/DocumentFile/' + os.path.basename(str(fetchQuery)))
#     fileName1Sentence = lstSentence

#     # fileName2
#     # chạy preprocess cho từng file trong fileName2
#     dataReadDoc = []
#     for fileUName in fileName2:
#         try:
#             # query database
#             querys = DataDocument.objects.filter(
#                 DataDocumentAuthor=str(userId)) \
#                 .filter(DataDocumentName=fileUName.split(".")[0]) \
#                 .filter(DataDocumentType=fileUName.split(".")[1])
#             fetchQuery = querys[0].DataDocumentFile
#             fName, lstSentence, lstLength = p.preprocess(
#                 settings.MEDIA_ROOT + '/DocumentFile/' + os.path.basename(str(fetchQuery)))
#             lst2 = lstSentence
#             dataReadDoc.append(lst2)
#         except Exception:
#             pass

#     # B2 trả json
#     # result so sánh
#     reportDataReadDoc = []
#     for i in range(len(dataReadDoc)):
#         result = ExportOrder(fileName1Sentence, dataReadDoc[i], rat)
#         reportDataReadDoc.append(result)
#     myDict = {}
#     myDict4 = []
#     listFileName = {}
#     myDict4 = makeDataStt(len(fileName2),dataReadDoc,reportDataReadDoc)

#     # line length list
#     listFileName = fileName2
#     myDict["file1"] = fileName1Sentence
#     myDict["ListFileName"] = listFileName
#     myDict["ListFile"] = myDict4
#     myDict["File1Name"] = fileName1
#     return Response(myDict, status=status.HTTP_200_OK)


# @api_view(('POST', 'GET'))
# def FinalCheck(request):
#     choice = request.data['choice']
#     filename = request.data['id']
#     if choice != None:
#         print(choice)
#         print(type(choice))
#         if choice == 1:
#             redirect('')
#         elif choice == 2:
#             print('database')
#             res = documentimportDatabase()
#             print('res is ------------------', res)
#             return Response(res, status.HTTP_200_OK)
#         elif choice == 3:
#             print('internet')
#             res = documentimportInternet(request.data)
#             print('res is ------------------', res)
#             return Response(res, status.HTTP_200_OK)
#         elif choice == 4:
#             res = documentimportDatabaseInternet(request.data)
#             return Response(res, status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     return Response(status=status.HTTP_200_OK)


# # upload 1 file
# @api_view(('POST',))
# def uploadDoc(request):
#     content = None
#     if request.method == 'POST':
#         id = request.data["id"]
#         form1 = UploadOneFileForm(request.POST, request.FILES)

#         if form1.is_valid():

#             # save form người dùng gửi
#             data = form1.cleaned_data
#             file1 = data['DataDocumentFile']  # abc.doc
#             file_name = file1.name.split(".")[0]  # doc
#             extension = file1.name.split(".")[-1]  # abc
#             content = file_name
#             data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=id, DataDocumentType=extension,
#                                 DataDocumentFile=file1)
#             data.save()
#             # data= form1.save(commit = False)

#             fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)
#             # //save to db//
#             length = len(lstSentence)
#             for i in range(length):
#                 c = data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i],
#                                                         DataDocumentSentenceLength=lstLength[i])

#             result = file_name + '.' + extension
#             res = result
#             content = {'filename': file1}
#             return Response(res, status=status.HTTP_200_OK)
#         else:
#             return Response(content, status=status.HTTP_204_NO_CONTENT)

#     else:
#         form = UploadOneFileForm()
#         content = {'please move along': 'have the same username'}
#         return Response(content, status=status.HTTP_204_NO_CONTENT)


# # upload multiple file
# @api_view(('POST', 'GET'))
# def uploadDocList(request):
#     # chuong trinh test
#     content = None
#     if request.method == 'POST':
#         id = request.data["id"]
#         listfile = request.FILES.getlist('DataDocumentFile')
#         filenameList = []
#         count = 0
#         for f in listfile:
#             # name = listname[count]
#             count = count + 1
#             file1: file
#             file1 = f  # abc.doc
#             file_name = file1.name.split(".")[0]  # doc
#             extension = file1.name.split(".")[-1]  # abc
#             filenameList.append(file1.name)

#             data = DataDocument(
#                 DataDocumentName=file_name,
#                 DataDocumentAuthor_id=id,
#                 DataDocumentType=extension,
#                 DataDocumentFile=file1
#                 )
#             data.save()

#         response = {'data': filenameList}

#         return JsonResponse(response, status=status.HTTP_200_OK)
#     else:
#         form = UploadManyFileForm()
#         content = {'please move along': 'have the same username'}
#         return Response(content, status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET'])
# def test(self):
#     main()
#     content = {'please move along': 'have the same username222'}
#     return Response(content, status=status.HTTP_200_OK)


# # rút data từ cursor rồi chuyển về dạng dict
# def dictfetchall(cursor):
#     desc = cursor.description
#     return [
#         dict(zip([col[0] for col in desc], row))
#         for row in cursor.fetchall()
#     ]


# # result
# # import mới


# # upload 1 file vo luu tru cau db cua he thong(khac userdb)
# def uploadDocumentSentenceToDatabase(request):
#     content = None
#     if request.method == 'POST':
#         id = request.data["id"]

#         form1 = UploadOneFileForm(request.POST, request.FILES)

#         if form1.is_valid():

#             # save form người dùng gửi
#             data = form1.cleaned_data
#             file1 = data['DataDocumentFile']  # abc.doc

#             file_name = file1.name.split(".")[0]  # doc
#             extension = file1.name.split(".")[-1]  # abc
#             content = file_name
#             data = DataDocument(DataDocumentName=file_name, DataDocumentAuthor_id=id, DataDocumentType=extension,
#                                 DataDocumentFile=file1)
#             data.save()
#             # data= form1.save(commit = False)

#             fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)
#             # //save to db//
#             length = len(lstSentence)
#             for i in range(length):
#                 c = data.datadocumentcontent_set.create(
#                     DataDocumentSentence=lstSentence[i],
#                     DataDocumentSentenceLength=lstLength[i]
#                     )

#             result = file_name + '.' + extension
#             res = result
#             content = {'filename': file1}

#             return Response(res, status=status.HTTP_200_OK)

#             # fake mocking
#         else:
#             # wrong form type
#             return Response(content, status=status.HTTP_204_NO_CONTENT)

#     else:
#         form = UploadOneFileForm()
#         content = {'please move along': 'have the same username'}
#         return Response(content, status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET'])
# def ff(self):
#     p.docx2txt("D:/project_doc.docx")


# # upload multiple file vo luu tru cau db cua he thong(khac userdb)
# def uploadMultipleDocumentSentenceToDatabase(request):
#     content = None
#     if request.method == 'POST':
#         id = request.data["id"]
#         listfile = request.FILES.getlist('DataDocumentFile')
#         filenameList = []
#         count = 0
#         for f in listfile:
#             # name = listname[count]
#             count = count + 1
#             file1: file
#             file1 = f  # abc.doc
#             file_name = file1.name.split(".")[0]  # doc
#             extension = file1.name.split(".")[-1]  # abc
#             filenameList.append(file1.name)

#             data = DataDocument(
#                 DataDocumentName=file_name,
#                 DataDocumentAuthor_id=id,
#                 DataDocumentType=extension,
#                 DataDocumentFile=file1
#                 )
#             data.save()

#             fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)
#             # //save to db//
#             length = len(lstSentence)
#             for i in range(length):
#                 c = data.datadocumentcontent_set.create(
#                     DataDocumentSentence=lstSentence[i],
#                     DataDocumentSentenceLength=lstLength[i]
#                     )

#         response = {'data': filenameList}

#         return JsonResponse(response, status=status.HTTP_200_OK)
#     else:
#         form = UploadManyFileForm()
#         content = {'please move along': 'have the same username'}
#         return Response(content, status=status.HTTP_204_NO_CONTENT)


# # up 1 file vao user db (chua xai)
# # uploadDoc3 old -> uploadOneDocUser (change name only)
# def jsonFile(request, file_name, userId):
#     filename = settings.MEDIA_ROOT + "/result/" + file_name + userId
#     # print("fullpath:          ", filename)
#     mydict = request
#     with open(filename + ".json", "w") as f:
#         json.dump(mydict, f)
#     fileJson = open(filename + ".json", "r")
#     # reportData = json.loads(fileJson.read())
#     # print(fileJson.name)
#     fileJson.close()
#     # os.remove(fileJson.name)
#     return fileJson.name


# @api_view(['GET'])
# def test(self):
#     main()
#     print('done')
#     content = {'please move along': 'have the same username222'}
#     return Response(content, status=status.HTTP_200_OK)

# # def testting(request):
# #     fileName1 = "bacho.docx"
# #     userId=3
# #     # 1 file access
# #     querys = DataDocumentT.objects.filter(
# #         DataDocumentAuthor=str(userId)
# #         ).filter(
# #         DataDocumentName=fileName1.split(".")[0]
# #         ).filter(
# #         DataDocumentType=fileName1.split(".")[1]
# #         )
# #     fetchQuery =querys[0].DataDocumentFile
# #     print("=======",fetchQuery," ",str(userId)," ",fileName1.split(".")[0]," ",fileName1.split(".")[1])
# #
# #     # 1 internet link access theo user
# #     internetTitle = "cau-6-trang-73-sgk-gdcd-11.jsp"
# #     querys = DataDocumentT.objects.filter(DataDocumentType="internet").filter(
# #         DataDocumentAuthor=str(userId))\
# #         .filter(DataDocumentName=internetTitle)
# #     # check all internet link
# #     # querys = DataDocumentT.objects.filter(
# #     #     DataDocumentType="internet"
# #     #     ).filter(
# #     #     DataDocumentName=internetTitle
# #     #     )
# #     fetchQuery =querys[0].DataDocumentFile
# #     print("=======",fetchQuery," ",str(userId)," ",fileName1.split(".")[0]," ",fileName1.split(".")[1])
# #     # check file exist
# #     print("======check=",querys.exists())
# #
# #     myDict={}


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
# def checkAgree(status, data):
#     agreeStatus = status
#     if (agreeStatus):
#         fName, lstSentence, lstLength = p.preprocess(
#             formatString(
#                 'DocumentFile',
#                 data.DataDocumentName,
#                 data.DataDocumentType))
#         # //save to db//
#         length = len(lstSentence)
#         for i in range(length):
#             a = data.datadocumentcontent_set.create(
#                 DataDocumentSentence=lstSentence[i],
#                 DataDocumentSentenceLength=lstLength[i])
#             print("a laf: \n",a)


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
    # print("line 837 ", FileString)
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
    for i in internetPage:
        if ("123doc" in i):
            internetPage.remove(i)
    for link in internetPage:
        if (internetKeywordSearch.is_downloadable(link)):
            # link_pdf.append(link)
            file_pdf = internetKeywordSearch.download_document(link)
            fName, lstSentence, lstLength = p.preprocess(file_pdf)
            data = DataDocument(
                DataDocumentName=link,
                DataDocumentAuthor_id=userId,
                DataDocumentType="internetPdf",
                DataDocumentFile=fName
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
            lstSentence = internetKeywordSearch.crawl_web(link)
            data = DataDocument(
                DataDocumentName=link,
                DataDocumentAuthor_id=userId,
                DataDocumentType="internet",
                DataDocumentFile=link
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
    print("data1: ",data1)
    data1["filenameA"], session = uploadDoc2(
                request.POST,request.FILES,request.data['id'],request.data["agreeStatus"])
    myDict, fileName1, userId = test1(data1, session)
    jsonFile(myDict, fileName1, userId, session)
    jsonData = readJson(session, userId)
    session1 = DocumentSession.objects.get(pk=session)
    session1.Status = True
    session1.save()
    return Response(status=status.HTTP_200_OK)


# kiểm vs internet
@api_view(('POST',))
def documentimportInternet(request):
    # fileName1 = request.data['fileName1']
    # userId = request.data['id']
    data1 = request.data
    print("data1: ",data1)
    data1["filenameA"], session = uploadDoc2(request.POST,request.FILES,request.data['id'],request.data["agreeStatus"])
    myDict, fileName1, userId = test2(data1, session)
    jsonFile(myDict, fileName1, userId, session)
    jsonData = readJson(session,userId)
    session1 = DocumentSession.objects.get(pk=session)
    session1.Status = True
    session1.save()
    #return Response(myDict, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)


@api_view(('POST',))
def documentimportDatabaseInternet(request):
    # fileName1 = request.data["fileName1"]
    # userId = int(request.data["id"])

    data1 = request.data
    data1["filenameA"], session = uploadDoc2(
        request.POST,request.FILES,request.data['id'],request.data["agreeStatus"])
    myDict1, fileName1, userId = test1(data1, session)
    myDict2, fileName1, userId = test2(data1, session)
    # myDict1 = test1(data1)
    # EmyDict2 = test2(data1)
    myDict = []
    myDict.append(myDict1)
    myDict.append(myDict2)
    jsonFile(myDict, fileName1, userId, session)
    jsonData = readJson(session, userId)
    session1 = DocumentSession.objects.get(pk=session)
    session1.Status = True
    session1.save()
    return Response(status=status.HTTP_200_OK)


# import mới
# dùng kiểm với data ng dùng
@api_view(('POST', 'GET'))
def documentimport(request):
    data1 = request.data
    #data1["filenameA"], session = uploadDoc(request)
    #data1["filenameB"] = uploadDocList(request, session)
    data1["filenameA"], session = uploadDoc2(
        request.POST,request.FILES,request.data['id'],request.data["agreeStatus"])

    data1["filenameB"] = uploadDocList2(
        request.POST,request.FILES,request.data['id'], session,request.data["agreeStatus"])
    myDict, fileName1, userId = test3(data1, session)
    jsonFile(myDict, fileName1, userId, session)
    jsonData = readJson(session, userId)
    session1 = DocumentSession.objects.get(pk=session)
    session1.Status = True
    session1.save()
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
    fileRatio = []
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
                fileRatio.append(result[1])

    myDict = {}
    myDict["AllFileRatio"] = fileRatio
    myDict["ListAllFile"]=[]
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
    print("filenmae: ", formatQuery('DocumentFile', os.path.basename(str(fetchQuery))))
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
    fileRatio = []
    for i in range(len(dataReadDoc)):
        result = ExportOrder4(fileName1Sentence, dataReadDoc[i], rat)
        reportDataReadDoc.append(result[0])
        fileRatio.append(result[1])
    myDict = {}
    myDict["file1"] = fileName1Sentence
    myDict["AllFileRatio"] = fileRatio
    myDict["ListAllFile"]=[]
    myDict["ListAllFile"].append(fileName1)
    myDict["ListAllFile"].extend(internetPage)

    myDict4 = makeData(len(internetPage), dataReadDoc, reportDataReadDoc)

    listFileName = internetPage
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
                .filter(DataDocumentType=fileUName.split(".")[1]) \
                .filter(SessionId=session)
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
    fileRatio = []
    for i in range(len(dataReadDoc)):
        result = ExportOrder4(fileName1Sentence, dataReadDoc[i], rat)
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
    myDict["ListAllFile"]=[]
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



def uploadDoc2(PostData,FileData,ID,agreeStatus):
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
        session = DocumentSession(NumOfFile=1,SessionUser=id)
        session.save()
        data = DataDocument(
            DataDocumentName=file_name,
            DataDocumentAuthor_id=id,
            DataDocumentType=extension,
            DataDocumentFile=file1,
            SessionId=session.id)

        data.save()

        # data= form1.save(commit = False)
        # agreeStatus = FileName if true, =0 if false
        if (agreeStatus):
            fName, lstSentence, lstLength = p.preprocess(
                formatString(
                    'DocumentFile',
                    data.DataDocumentName,
                    data.DataDocumentType))
            print("formatstring: ",formatString('DocumentFile',
                    data.DataDocumentName,
                    data.DataDocumentType))
            print("data.id la: ",data.id)
            # //save to db//
            length = len(lstSentence)
            for i in range(length):
                a = data.datadocumentcontent_set.create(
                    DataDocumentSentence=lstSentence[i],
                    DataDocumentSentenceLength=lstLength[i])
                print("a la: ",a.DataDocumentNo_id)
        result = file_name + '.' + extension
        content = {'filename': file1}
        print("result là: ",result, session.id)
        return result, session.id



def uploadDocList2(PostData,FileData,ID, session,agreeStatus):
    # chuong trinh test
    content = None
    print("session la: ",session)
    id = ID
    listfile = FileData.getlist('DataDocumentFile')
    filenameList = []
    count = 0
    session = DocumentSession.objects.get(pk=session)
    session.NumOfFile = 1 + len(listfile)
    session.save()
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
            DataDocumentFile=file1,
            SessionId=session.id
        )
        data.save()
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
    print("thong tin là: ",userId,file_name,session)
    temp=DataDocument.objects.filter(DataDocumentAuthor=str(userId))\
        .filter(DataDocumentName=file_name.split(".")[0])\
        .filter(SessionId=str(session))\
        .filter(DocumentStatus=True)
    print("temp la: ",temp)
    idFile=temp[0].id
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
    temp=DataDocument.objects.filter(DataDocumentAuthor=str(userId))\
        .filter(SessionId=str(session))\
        .filter(DocumentStatus=True)
    idFile=temp[0].id
    data=ReportDocument.objects.get(DocumentJson_id=idFile)
    fileJson = open(data.JsonFile, "r")
    reportData = json.loads(fileJson.read())
    fileJson.close()
    #os.remove(fileJson.name)
    print("report data là: ",reportData)
    return reportData

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


#update 26/5/2021 -- 22h51