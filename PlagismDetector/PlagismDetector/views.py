from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader
from django.urls import reverse
from django.views import generic
#cần import cho db
from .models import DataDocument, DataDocumentContent
from django.db import connection
from django.db.models import Q
#can import cho levenshtein
from .Levenshtein import *
#cần import cho up file
from django.core.files.storage import FileSystemStorage
from .form import DocumentForm
from django.conf import settings
#import cho tách câu
import os
import sys
sys.path.append(os.getcwd()+'\\polls\\preprocessing')
from .preprocessing import preprocessor as p
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
def documentimport(request):
    # đọc data từ database
    #posts = DataDocumentContent.objects.all()
    cursor = connection.cursor()
    #cursor.execute("SELECT DataDocumentSentence,DataDocumentNo_id  FROM polls_datadocumentcontent WHERE DataDocumentSentence='ABCDEF 123'")
    cursor.execute("SELECT DataDocumentSentence FROM polls_datadocumentcontent WHERE DataDocumentNo_id='1';")
    
    posts = dictfetchall(cursor)
    #list of dicts to list of value (chuyển đổi)
    a_key = "DataDocumentSentence"
    # list 1 lấy từ database
    lst1 = [a_dict[a_key] for a_dict in posts]
    # list 2 user upload, lấy file rồi dùng proccessor, sau đó so sánh
    dataFromFile= DataDocument.objects.get(pk=22)
    
    fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + dataFromFile.DataDocumentName+ '.'+dataFromFile.DataDocumentType)
    #print(lstSentence)
    lst2 = lstSentence
    #list of dicts to list of value end
    result = Matching_ratio_list(lst2, lst1)
    report = Export(result, lst2, lst1)

    print(connection.queries)
    return render(request,'polls/output.html',{'data': report})


#upload 1 file
def uploadDoc(request):
    if request.method=='POST':
        form1 = DocumentForm(request.POST, request.FILES)
        if form1.is_valid():
            # save form người dùng gửi
            data= form1.save()
            
            # sử dụng preprocessor và lưu vào database
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName+'.'+ data.DataDocumentType)
            
            #//save to db//  
            length= len(lstSentence)
            for i in range(length):
                c=data.datadocumentcontentt_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
                print(c)
            return HttpResponseRedirect('http://127.0.0.1:4200/')
            
    else:
        form = DocumentForm()
    return render(request,'polls/upload.html',{
        'form':form
    })
