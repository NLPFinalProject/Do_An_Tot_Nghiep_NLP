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

import pickle
from Levenshtein import *
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from MailComponent import views as mail
import random as rand

# Create your views here.
@api_view([ 'POST'])
def ExportResult(request):
    data = request.data
    mail.sendExportMail(data)
    return Response(status=status.HTTP_200_OK)

    