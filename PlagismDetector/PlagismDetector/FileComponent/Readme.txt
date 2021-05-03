# 13/4/2021
# them ham exportorder3 vao levenshtein
def ExportOrder3(lst_1, lst_2, ratio):
    result = []
    length = 0

    for i in range(len(lst_1)):
        export = {}
        similar_sent = []
        count = 0
        for j in range(len(lst_2)):
            if Matching_ratio(lst_1[i], lst_2[j]) >= ratio:
                count += 1
                similar_sent.append(j + 1)
        
        if count != 0:
            length += 1
            export['line'] = i + 1
            export['count'] = count
            export['lst'] =similar_sent
            result.append(export)
    
    return result, length/len(lst_1)*100

# them ham tim kiem he thong + internet
#systemSearch
def documentimportDatabase(request):
    print('------------------------------')
    fileName1 = "tndl.docx"
    userId=3
    fileName2Sentence=[]

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
    print("---tag---",type(tagPage),tagPage)
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
    for idFile in idStatistic.items():
        print(idFile[0])
        if (countReport<1):
            queryRaw ="SELECT DataDocumentSentence FROM `filecomponent_datadocumentcontent` WHERE DataDocumentNo_id="+str(idFile[0])+";"
            print("=====",queryRaw)
            cursor.execute(queryRaw)
            fetchQuery = dictfetchall(cursor)
            fileName2Sentence = [a_dict["DataDocumentSentence"] for a_dict in fetchQuery]
            result = ExportOrder3(fileName2Sentence, fileName1Sentence,70)
            if (result[1]>=70 and countReport<1):
                countReport+=1
                reportIdFile.append(idFile[0])
                reportDataReadDoc.append(result[0])
                ReportFileName2Sentence.append(fileName2Sentence)

    
    
    

    myDict = {}
    myDict2 = {}
    myDict["file1"] = fileName1Sentence
    for i in range(countReport):
        mydic3={}
        mydic3["list"+str(reportIdFile[i])]=ReportFileName2Sentence[i]
        mydic3["stt"]=reportDataReadDoc[i]
        myDict2[str(reportIdFile[i])]=mydic3
    
    # report cac cau html
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
    # result so sanh
    reportDataReadDoc=[]
    for i in range(len(dataReadDoc)):
        result = ExportOrder2(fileName1Sentence, dataReadDoc[i],70)
        reportDataReadDoc.append(result)

    myDictHtml2 = {}
    myDict["file1"] = fileName1Sentence
    for i in range(len(internetPage)):
        mydic3={}
        mydic3["list"+internetPage[i]]=dataReadDoc[i]
        mydic3["stt"]=reportDataReadDoc[i]
        myDictHtml2[internetPage[i]]=mydic3

    #line length list
    myDict["fileName2"]=myDict2
    myDict["internet"]=myDictHtml2
    # print(connection.queries)
    return render(request,'polls/output.html',{'data': myDict})
