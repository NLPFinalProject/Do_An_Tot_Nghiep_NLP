from django.shortcuts import render 
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.core.mail import EmailMessage
from UserComponent.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
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
from MailComponent import views as mail
from FileComponent.models import DocumentSession,DataDocument
import random as rand
from rest_framework_jwt.views import obtain_jwt_token as obtainToken
from rest_framework_jwt.views import ObtainJSONWebToken,JSONWebTokenSerializer

class NewAPILogin(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        content = None
        response = super().post(request, *args, **kwargs)
        try:
            user = User.objects.get(username=  request.data['username'])
            userStatus = UserSerializer(user)
            user = userStatus.data
            if user['is_lock'] == True:
                content = {'data': "Tài khoản đang bị khóa"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            elif user['is_active'] == False:
                content = {'data': "Tài khoản chưa được kích hoạt"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                return response
        except:
            return response
        
       

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
        DateOfBirth = request.data["ngaySinh"])
        number = mail.sendVerificationMail(request.data["email"])
        user.set_password(user.password)
        user.save()
        users = UserSerializer(user)
        #print(users.data)
        response = {'data' : users.data,'validCode' : number}
        return JsonResponse(response,status = status.HTTP_200_OK)

@api_view([ 'POST','GET','PUT'])
def APIUser(request):
    #post user = save user with user
    if request.method =='POST':
    
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
            user.set_password(user.password)
            user.save()
            users = UserSerializer(user)
            print(users.data)
            response = {'data' : users.data,'validCode' : number}
            return JsonResponse(response,status = status.HTTP_200_OK)
    elif request.method == 'GET':
        try:
            #if get user successfull
            user = User.objects.get(username = request.data["id"])
            return JsonResponse(user,status=status.HTTP_200_OK)
        #in case we don't have any user match the request
        except ObjectDoesNotExist:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        #put user = change user profile
    elif request.method == 'PUT':
        try:
            user = User.objects.get(username = request.PUT["email"])
            #password = request.data["password"],
            user.name = request.PUT["fullName"],
            user.EmailOrganization = request.PUT["emailOrganization"],
            user.phone = request.PUT["phoneNumber"],
            user.DateOfBirth = request.PUT["ngaySinh"]
            #user.set_password(user.password)
            user.save()
            users = UserSerializer(user)
            print(users.data)
            response = {'data' : users.data}
            return JsonResponse(response,status = status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        

    
    

@api_view([ 'GET','POST'])
def isAdmin(request):
    #if(request.data not None)
    
    try: 
        user = User.objects.get(username = request.GET['username'])
        response = {'isAdmin' : user.is_admin}
        return JsonResponse(response,status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
         return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

@api_view([ 'POST'])
def ActivateUser(request):
    #if(request.data not None)
    print(request.data)
    userinfo =  request.data["userinfo"]
    print(request.data['confirmpassword'])
    print( request.data['valicode'])
    print(type(request.data['valicode']))
    print(type(request.data['confirmpassword']))
    if request.data['confirmpassword'] == str(request.data['valicode']):
        user = User.objects.get(username = userinfo['username'])
        print(user.username)
        user.is_active = True
        user.active = True
        user.save()
        return HttpResponse(status=status.HTTP_200_OK)
    else:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
@api_view([ 'POST'])
def ResetPassword(request):
    #if(request.data not None)
    try:
        user = User.objects.get(username = request.data["username"])
        flag = user.check_password(request.data['password'])
        if flag==False:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.data['reset'])
        #user.password = request.data['password']
        user.save()
        return HttpResponse(status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        content = "username or password is wrong, please try again"
        return Response(content,status=status.HTTP_400_BAD_REQUEST)
@api_view([ 'POST'])
def ForgetPassword(request):
    #if(request.data not None)
    try:
        user = User.objects.get(username = request.data["username"])
        print(user.username)
        emailPassword = mail.sendNewPasswordEmail(request.data["username"])
        user.set_password(str(emailPassword))
        user.save()
        return HttpResponse(status=status.HTTP_200_OK)
    except:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    
@api_view([ 'POST','GET'])
def UserList(request):
    userList=User.objects.all()
    
    users = []
    for user in userList:
        newUser  = UserSerializer(user)
        users.append(newUser.data)
    content = {"users":users}
    print(content)
    #idFile=temp[0].id
    #data=
    
    return Response(content, status=status.HTTP_200_OK)  
@api_view([ 'POST','GET']) 
def lockUser(request):
    """for admin, fix later
    isAdmin = request.GET('isAdmin')
    if isAdmin == False
    return HttpResponse(status=status=status.HTTP_400_BAD_REQUEST)
    """
    username = request.GET['username']
    user = User.objects.get(username = username)
    # if statement
    user.is_lock=TRUE
    user.save()
    return HttpResponse(status=status.HTTP_200_OK)
@api_view([ 'POST','GET']) 
def unlockUser(request):
    """for admin, fix later
    isAdmin = request.GET('isAdmin')
    if isAdmin == False
    return HttpResponse(status=status=status.HTTP_400_BAD_REQUEST)
    """
    username = request.GET['username']
    user = User.objects.get(username = username)
    # if statement
    user.is_lock=False
    user.save()
    return HttpResponse(status=status.HTTP_200_OK)
@api_view(['POST'])
def login(request):
    content = None
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

@api_view(('GET',))
@permission_classes([IsAuthenticated])
def Session(request):
   
    content =None
    userId = request.GET['id']
    try:
        # session=DocumentSession.objects.filter(SessionUser=str(userId))
        # content = session
        session = readSession(userId)
        print(session)
        # print("session là: ",content)
        content ={"session":session} 
        return Response(content,status=status.HTTP_200_OK)  
    except ObjectDoesNotExist:
        return Response(None, status=status.HTTP_200_OK)


def readSession(userId):
    sessionList = DocumentSession.objects.filter(SessionUser=str(userId))
    ResponseContent = []
    for i in range(len(sessionList)):
        temp = {}
        query1 = DataDocument.objects.filter(
            DataDocumentAuthor=str(sessionList[i].SessionUser)) \
            .filter(SessionId=str(sessionList[i].id))
        query2 = DocumentSession.objects.get(pk=sessionList[i].id)
        if (query2.Status == "Loading"):
            success = query2.ChildReport
            loading = len(query1) - success
            fail = 0
        else:
            success = query2.ChildReport
            fail = len(query1) - success
            loading = 0
        #temp1 = [success, loading, fail]
        temp1 = {}
        temp1["success"]= success
        temp1["loading"]=loading
        temp1["fail"] = fail
        temp["ChildReport"] = temp1
        temp["Status"] = sessionList[i].Status
        temp["id"] = sessionList[i].id
        temp["NumOfFile"] = sessionList[i].NumOfFile
        temp["Date"] = sessionList[i].Date
        temp["SessionUser"] = sessionList[i].SessionUser
        temp["SessionName"] = sessionList[i].SessionName
        temp["SessionType"] = sessionList[i].SessionType
        querys = DataDocument.objects.filter(
            DataDocumentAuthor=str(sessionList[i].SessionUser)) \
            .filter(SessionId=str(sessionList[i].id))
        # temp['filename'] = querys[0].DataDocumentName
        # ResponseContent.append(temp) 
        temp2 = []
        for j in range(len(querys)):
            temp2.append(querys[j].DataDocumentName)
        temp["filename"] = temp2
        ResponseContent.append(temp)

    return ResponseContent
@api_view(['GET'])
def GetProfile(request):
    try:

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