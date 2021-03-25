from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader
from django.urls import reverse
from django.views import generic
#cần import cho db
from .models import Question, Choice, DataDocument, DataDocumentContent, DataDocumentT, DataDocumentContentT
from django.db import connection, connections
from django.db.models import Q
#can import cho levenshtein
from .Levenshtein import *
#from .Levenshtein1 import *
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

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/show.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/vote.html', {
            'question': question,
            'error_message': "You haven't select a choice yet.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

#demo showcase
def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        #docT= DataDocumentT.objects.get(pk=1)
        #print(settings.MEDIA_ROOT +'\\DocumentFile\\' + docT.DataDocumentName)
        #fName,lstsentence,c = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + docT.DataDocumentName+ '.docx')
        #//save to db//  
        #q.save()
        #q= DataDocument(DataDocumentName=fName, DataDocumentType ="docx", DataDocumentAuthor = fs.)
        #length= len(lstsentence)
        #for i in range(length):
        #c=q.datadocumentcontent_set.create(DataDocumentSentence=lstsentence[i], DataDocumentSentenceLength=c[i])
        #    c=q.datadocumentcontentt_set.create(DataDocumentSentence=lstsentence[i], DataDocumentSentenceLength=c[i])
    return render(request,'polls/upload.html')
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
    #query tu ourdatabase
    cursor = connections['testDb3'].cursor()
    #cursor.execute("SELECT DataDocumentSentence,DataDocumentNo_id  FROM polls_datadocumentcontent WHERE DataDocumentSentence='ABCDEF 123'")
    cursor.execute("SELECT DataDocumentSentence FROM polls_datadocumentcontentt WHERE DataDocumentNo_id='1';")
    
    posts = dictfetchall(cursor)
    #list of dicts to list of value (chuyển đổi) start|||
    a_key = "DataDocumentSentence"
    # list 1 lấy từ database
    lst1 = [a_dict[a_key] for a_dict in posts]
    # list 2 user upload, lấy file rồi dùng proccessor, sau đó so sánh

    # đọc nhiều file trong userdb = default
    dataReadDoc = []
    for i in range(35,36):
        try:
            dataFromFile= DataDocumentT.objects.get(pk=i)
        
            print("file access la ----",i,"-----",settings.MEDIA_ROOT +'\\DocumentFile\\' + dataFromFile.DataDocumentName)
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + dataFromFile.DataDocumentName+ '.'+dataFromFile.DataDocumentType)
            lst2 = lstSentence
            dataReadDoc.append(lst2)
        except Exception:
            pass

        
        
    print("____dataReadDoc la _____",dataReadDoc)
    # đọc 1 file từ userdb = default
    dataFromFile= DataDocumentT.objects.get(pk=22)
    #print("file access la ---------",settings.MEDIA_ROOT +'\\DocumentFile\\' + dataFromFile.DataDocumentName)
    fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + dataFromFile.DataDocumentName+ '.'+dataFromFile.DataDocumentType)
    #print(lstSentence)
    #lst2 = ['Mặt trời xuống biển như hòn lửa.','Sóng đã cài then, đêm sập cửa.','Đoàn thuyền đánh cá lại ra khơi.','Câu hát căng buồm cùng gió khơi.']
    lst2 = lstSentence
    #list of dicts to list of value endcode|||

    # mảng result so sánh
    reportDataReadDoc=[]
    for i in range(len(dataReadDoc)):
        result = Matching_ratio_list(dataReadDoc[i], lst1)
        report = Export(result, dataReadDoc[i], lst1)
        reportDataReadDoc.append(report)

    # result so sánh mẫu
    result = Matching_ratio_list(lst2, lst1)
    report = Export(result, lst2, lst1)
    #print(lst1)
    #print(report)
    print("_______nội dung report ======== ",reportDataReadDoc)
    print(connection.queries)
    return render(request,'polls/output.html',{'data': reportDataReadDoc})

def book_list(request):
    #docT= DataDocumentT.objects.get(pk=1)
    #fName,lstsentence,c = p.preprocess(docT.DataDocumentName)
    return render(request,'polls/show.html')

# dta=[]
#upload 1 file
def uploadDoc(request):
    if request.method=='POST':
        form1 = DocumentForm(request.POST, request.FILES)
        if form1.is_valid():
            # save form người dùng gửi
            data= form1.save(commit=False)
            # listFieldData=[data.DataDocumentName,data.DataDocumentAuthor,data.DataDocumentType,data.DataDocumentFile]
            
            # key_1 = "DataDocumentName"
            # key_2 = "DataDocumentAuthor"
            # key_3 = "DataDocumentType"
            # key_3 = "DataDocumentFile"
            # dic = {}
            # dic[key_1] = data.DataDocumentName
            # dic[key_2] = data.DataDocumentAuthor
            # dic[key_3] = data.DataDocumentType
            # dic[key_3] = data.DataDocumentFile
            # dta.append(dic)
            # for dictInDta in dta:
            data.DataDocumentAuthor="red"
            data.DataDocumentName=str(data.DataDocumentFile).split("/")[-1].split(".")[-2]
            data.DataDocumentType=str(data.DataDocumentFile).split("/")[-1].split(".")[-1]
            data.save(using='testDb3')
            print("data---name----------===111 ----- ",str(data.DataDocumentFile).split("/")[-1])
            print("data----duoi---------===111 ----- ",str(data.DataDocumentFile).split("/")[-1].split(".")[-1])
            print("data la -----------------------------",data.pk,data.DataDocumentName,data.DataDocumentType)
            print(settings.MEDIA_ROOT +'\\DocumentFile\\'  + str(data.DataDocumentFile).split("/")[-1])       
            #extacting word -> save db
            #cach1
            #data==q = DataDocumentT.objects.get(pk=1)
            #q.datadocumentcontentt_set.all()
            #c=q.datadocumentcontentt_set.create(DataDocumentSentence="Thuyền ta lái gió với buồm trăng.", DataDocumentSentenceLength=33)           
            #cach2
            #data==docT= DataDocumentT.objects.get(pk=1)
            #print(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName)

            # sử dụng preprocessor và lưu vào database
            # fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + str(data.DataDocumentFile).split("/")[-1])
            # #print(lstSentence)
            # print("name la ==========11=22== ",fName,"===",lstLength)

            #//save to db//  
            # length= len(lstSentence)
            # for i in range(length):
            #     c=data.datadocumentcontentt_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
            #     print(c)
            return HttpResponseRedirect('http://127.0.0.1:8000/polls/')
            
    else:
        form = DocumentForm()
    return render(request,'polls/upload.html',{
        'form':form
    })

#upload n file
def uploadDocMultiple(request):
    if request.method=='POST':
        form1 = DocumentForm(request.POST, request.FILES)
        if form1.is_valid():
            # save form người dùng gửi
            data= form1.save(commit=False)
            print("data la -----------------------------",data.pk,data.DataDocumentName,data.DataDocumentType)
            print(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName)       
            #extacting word -> save db
            #cach1
            #data==q = DataDocumentT.objects.get(pk=1)
            #q.datadocumentcontentt_set.all()
            #c=q.datadocumentcontentt_set.create(DataDocumentSentence="Thuyền ta lái gió với buồm trăng.", DataDocumentSentenceLength=33)           
            #cach2
            #data==docT= DataDocumentT.objects.get(pk=1)
            #print(settings.MEDIA_ROOT +'\\DocumentFile\\' + data.DataDocumentName)

            # sử dụng preprocessor và lưu vào database
            fName,lstSentence,lstLength = p.preprocess(settings.MEDIA_ROOT +'\\DocumentFile\\' + str(data.DataDocumentFile).split("/")[-1])
            print(lstSentence)
            print("name la ==========11=22== ",fName)
            #//save to db//  
            length= len(lstSentence)
            for i in range(length):
                c=data.datadocumentcontentt_set.create(DataDocumentSentence=lstSentence[i], DataDocumentSentenceLength=lstLength[i])
                print(c)
            return HttpResponseRedirect('http://127.0.0.1:8000/polls/')
            
    else:
        form = DocumentForm()
    return render(request,'polls/upload.html',{
        'form':form
    })