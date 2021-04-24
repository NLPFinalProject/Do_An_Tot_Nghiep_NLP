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

@api_view([ 'POST'])
#@permission_classes ( (AllowAny, ))

@csrf_exempt
def register(request):
    
    try:
        user = User.objects.get(username = request.data["email"])
        content = {'data': 'username is existed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
    except ObjectDoesNotExist:
        print(request.data["phoneNumber"])
        user = User.objects.create(username = request.data["email"],
        password = request.data["password"],
        name = request.data["fullName"],
        EmailOrganization = request.data["emailOrganization"],
        phone = request.data["phoneNumber"],
        is_active = False,
        DateOfBirth = request.data["ngaySinh"],)
        number = CreateValidateCode()
        email = EmailMessage(
        'Hello',
        'this is a confirmnation mail, please enter the code below'+str(number),
        'kaitouthuan@gmail.com',
        [user.username], 
        headers={'Message-ID': 'foo'},)
        email.send()
        user.set_password(user.password)
        user.save()
        users = UserSerializer(user)
        users.data.key = '1243'
        print(users.data)
        response = {'data' : users.data,'validCode' : '1243'}
        return JsonResponse(response,status = status.HTTP_200_OK)
    #else:
        

    
    
        #return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        # In order to serialize objects, we must set 'safe=False'

@api_view([ 'POST'])
def ActivateUser(request):
    #if(request.data not None)
    
    
    user = User.objects.get(username = request.data["username"])
    print(user.username)
    user.is_active = True
    user.active = True
    user.save()
   
    return HttpResponse(status=status.HTTP_200_OK)

@api_view([ 'POST'])
def ResetPassword(request):
    #if(request.data not None)
    
    
    user = User.objects.get(username = request.data["username"])
    print(user.username)
    print(user.password)

    
    user.password = request.data.password
    user.save()
    return HttpResponse(status=status.HTTP_200_OK)
@api_view([ 'POST'])
def ForgetPassword(request):
    #if(request.data not None)
    
    
    user = User.objects.get(username = request.data["username"])
    print(user.username)
    user.password = '12543'
    user.save()
    email = EmailMessage(
    'Hello,Your new password is now 12543',
    
    'kaitouthuan@gmail.com',
    [user.username], 
    headers={'Message-ID': 'foo'},)
    email.send()
    content =''
    return HttpResponse(status=status.HTTP_200_OK)

    
@api_view(['POST'])
def login(request):
    content = None
    print(request.data["username"])
    print(request.data["password"])
    
    try:
        user = User.objects.get(username = request.data["username"])
        
        if user.check_password(request.data["password"]):
            if user.is_active == True:
                users = UserSerializer(user)
                return Response(users.data,status=status.HTTP_200_OK)
            else:
                content="account hasn't been active yet,please activate it"
                return JsonResponse(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            content = "wrong password, please try again"
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    except ObjectDoesNotExist:
        content = "username or password is wrong, please try again"
        return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    # In order to serialize objects, we must set 'safe=False'

   
@api_view(['POST'])
def fakelogin(request):
    content = None
    print('fake login is here')
    return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

@api_view(['GET'])
def GetProfile(request):
    try:
        print('---------------------')
    
    
        print(request.body)
        print('---------------------')
        user = User.objects.get(username=  request.GET.get('username'))
        users =UserSerializer(user)
        return Response(users.data, status=status.HTTP_200_OK)
        
    except ObjectDoesNotExist:
        return Response(None, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    
        

def ConvertData(request):
    user = User.objects.all()
    user.username = request.data["email"]
    user.password = request.data["password"]
    user.name = request.data["fullName"]
    user.EmailOrganization = request.data["emailOrganization"]
    user.phone = request.data["phoneNumber"]
    user.active = False
    user.DateOfBirth = request.data["ngaySinh"]
    return user
def CreateValidateCode():
    number = rand.randrange(1000, 9999)
    return number
@api_view([ 'POST'])
@csrf_exempt
def UpdateUser(request):
    
    try:
        print(request.data)
        user = User.objects.get(username = request.data["email"])
        
        
        user.name = request.data["fullName"]
        user.EmailOrganization = request.data["emailOrganization"]
        user.phone = request.data["phoneNumber"]
        
        user.DateOfBirth = request.data["ngaySinh"]
        
        
        user.save()
        users = UserSerializer(user)
        users.data.key = '1243'
        print(users.data)
        response = {'data' : users.data,'validCode' : '1243'}
        return JsonResponse(response,status = status.HTTP_200_OK)
        
    except ObjectDoesNotExist:
        
        
        content = {'please move along': 'have the same username'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)
    #else: