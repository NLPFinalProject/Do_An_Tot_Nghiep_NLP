# hàm preprocessor
# thêm hàm này vào
def para2txt(list_para):
    split_sentence = []  ## list chứa danh sách câu được tách ra. mỗi phần tử là 1 câu.
    for para in list_para:
        split_sentence.extend(vncorenlp.pos_tag(para))  
    return split_sentence  # update: trả ra pos_tag là có gán nhãn cho tưng từ về loại từ.

# hàm TF-IDF
# thêm hàm này vào
from bs4 import BeautifulSoup
def crawl_web(link):
    news=requests.get(link)
    soup=BeautifulSoup(news.content,"html.parser")
    lst_text=list(filter(str.strip,soup.get_text().split("\n")))
    return lst_text

# views documentimportInternet
# từ print("---tag---",type(tagPage),tagPage)
# cho tới os.remove(file_pdf)
# thay bằng đoạn ở dưới
# phần mydic chỗ nào có filename2 đổi thành internetPage
print("---tag---",type(tagPage),tagPage)
    #internet search
    internetPage2 = internetKeywordSearch.get_link(tagPage,fName,lstSentence,lstLength)
    fileName1Sentence = lstSentence
    internetPage = [internetPage2[i] for i in range(3)]
    print("_______nội dung report ======== ",internetPage)
    link_pdf=[]
    link_html=[]
    # report cac cau html
    dataReadDoc=[]
    for link in internetPage:
        if('.pdf'in link):
            #link_pdf.append(link)
            file_pdf=internetKeywordSearch.download_pdf(link)
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
            lstSentence=p.convert2listsen(p.para2txt(internetKeywordSearch.crawl_web(link)))
            data = DataDocument(DataDocumentName=link, DataDocumentAuthor_id=3,DataDocumentType="internet", DataDocumentFile=link)
            data.save()
            dataReadDoc.append(lstSentence)
            # length= len(lstSentence)
            # for i in range(length):
            #     c=data.datadocumentcontent_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=len(lstSentence[i]))
            #     #print(c)