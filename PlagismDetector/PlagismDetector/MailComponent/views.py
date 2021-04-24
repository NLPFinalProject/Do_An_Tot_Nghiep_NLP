from django.shortcuts import render

# Create your views here.
from django.shortcuts import render 
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.core.mail import EmailMessage
from UserComponent.models import User
from rest_framework.decorators import api_view
from UserComponent.serializers import UserSerializer
from tkinter import *
from tkinter import messagebox
import pickle
from Levenshtein import *
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import TokenAuthentication
import random as rand
import os
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
def sendVerigicationMail(email):
    number = CreateValidateCode()
    email = EmailMessage(
            'Hello',
            'this is a confirmnation mail, please enter the code below'+str(number),
            #user.username
            'ldthuan1907@gmail.com',
            [email], 
            headers={'Message-ID': 'foo'},)
            #email.send()
            
    response = {'data' : None,'validCode' : number}

def sendExportMail(data):
    localsite = 'http://localhost:4200/checkresult/result'
    print(data)
    linkfile = os.getcwd() + '/MailComponent/mail_template.html'
    dataname = data['name']
    datahitrate = data['HitRate']
    dataid =  data['id']
    datacount = data['count']
    File1Name = data['File1Name']
    
    linktoFile = []
    tmp={}
    list =[]
    for i in range(len(dataname)):
        dicttmp={}
        dicttmp['name']=dataname[i]
        dicttmp['HitRate']=datahitrate[i]
        dicttmp['count']=datacount[i]
        link = localsite+'?filename1='+File1Name+'&listfile='+dataname[i]+'&id='+dataid
        dicttmp['link']=link
        #dicttmp['link']='localhost:/4200/daovan'
        tmp = dicttmp
        
        list.append(tmp)
    #list.append(tmp)
    #for i in list
    print(list)
    html_message = render_to_string('mail_template.html', {'data':list})
    print(html_message)
    id = data['id']
    
    plain_message = strip_tags(html_message)
    """email = EmailMessage(
            'Hello',
            plain_message,
            'ldthuan1907@gmail.com',
            ['kaitouthuan@gmail.com'], 
            html_message=html_message,
            headers={'Message-ID': 'foo'},)
     """   

    mail.send_mail('Hello', plain_message, 'kaitouthuan@gmail.com', ['ldthuan1907@gmail.com'], html_message=html_message)

            
            
