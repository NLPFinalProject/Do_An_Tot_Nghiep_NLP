# 13/4/2021
# copy file TF-IDF.py moi, thay vao cai cu
# su dung preprocessor ban moi nhat
# copy paste phan report cac cau html o duoi
# thay vao doan tuong ung trong documentImportInternet

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