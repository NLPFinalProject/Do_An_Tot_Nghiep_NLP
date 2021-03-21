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
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
@api_view([ 'POST'])
def SendEmail(request):
    
    try:
        user = User.objects.get(username = request.data["email"])
        content = {'please move along': 'have the same username'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)
        
    except ObjectDoesNotExist:
        user = User.objects.create(username = request.data["email"],
        password = request.data["password"],
        name = request.data["fullName"],
        EmailOrganization = request.data["emailOrganization"],
        phone = request.data["phoneNumber"],
        active = False,
        DateOfBirth = request.data["ngaySinh"],)
        email = EmailMessage(
        'Hello',
        'this is a confirmnation link http://google.com',
        'kaitouthuan@gmail.com',
        [user.username], 
        headers={'Message-ID': 'foo'},)
        email.send()
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
    user.active = True
    user.save()
   
    return HttpResponse(status=status.HTTP_200_OK)

@api_view([ 'POST'])
def ResetPassword(request):
    #if(request.data not None)
    
    
    user = User.objects.get(username = request.data["username"])
    print(user.username)
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
    'Hello,Yourn new password is now 12543',
    
    'kaitouthuan@gmail.com',
    [user.username], 
    headers={'Message-ID': 'foo'},)
    email.send()
    content =''
    return HttpResponse(status=status.HTTP_200_OK)
@csrf_exempt
def customer_list(request):
    if request.method == 'POST':
        email = EmailMessage(
        'Hello',
        'Body goes here',
        'kaitouthuan@gmail.com',
        [request.email.value], 
        headers={'Message-ID': 'foo'},)
        return "None"
       
        #return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        # In order to serialize objects, we must set 'safe=False'

    
    elif request.method == 'DELETE':
        User.objects.all().delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt 
def customer_detail(request, pk):
    try: 
        User = User.objects.get(pk=pk) 
    except User.DoesNotExist: 
        return HttpResponse(status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        User_serializer = UserSerializer(User) 
        return JsonResponse(User_serializer.data) 
 
    elif request.method == 'PUT': 
        User_data = JSONParser().parse(request) 
        User_serializer = UserSerializer(User, data=User_data) 
        if User_serializer.is_valid(): 
            User_serializer.save() 
            return JsonResponse(User_serializer.data) 
        return JsonResponse(User_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        User.delete() 
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    
@csrf_exempt
def customer_list_age(request, age):
    Users = User.objects.filter(age=age)
        
    if request.method == 'GET': 
        Users_serializer = UserSerializer(Users, many=True)
        return JsonResponse(Users_serializer.data, safe=False)
        # In order to serialize objects, we must set 'safe=False'
    
@api_view(['POST'])
def login(request):
    content = None
    print(request.data["username"])
    print(request.data)
    try:
        user = User.objects.get(username = request.data["username"])

        if user.password == request.data["password"]:
            if user.active == True:
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