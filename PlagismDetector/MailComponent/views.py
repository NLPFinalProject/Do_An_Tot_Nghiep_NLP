# Create your views here.
import os
import random as rand

from django.core import mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from UserComponent.models import User


def CreateValidateCode():
    number = rand.randrange(100000, 999999)
    return number


def sendVerificationMail(email):
    number = CreateValidateCode()
    email = EmailMessage(
        'Hello',
        'this is a confirmnation mail, please enter the code below ' + str(number),
        # user.username
        'kaitouthuan@gmail.com',
        [email],
        headers={'Message-ID': 'foo'}, )
    email.send()

    return number


def sendNewPasswordEmail(email):
    number = CreateValidateCode()
    email = EmailMessage(
        'Hello',
        'Your new password is ' + str(number),
        # user.username
        'kaitouthuan@gmail.com',
        [email],
        headers={'Message-ID': 'foo'}, )
    email.send()

    return number


def sendExportMail(data):
    localsite = 'http://localhost:4200/checkresult/result'
    linkfile = os.getcwd() + '/MailComponent/mail_template.html'
    dataname = data['name']
    datahitrate = data['HitRate']
    dataid = data['id']
    user = User.objects.get(id=data["id"])
    datacount = data['count']
    File1Name = data['File1Name']

    list = []
    for i in range(len(dataname)):
        dicttmp = {}
        dicttmp['name'] = dataname[i]
        dicttmp['HitRate'] = datahitrate[i]
        dicttmp['count'] = datacount[i]
        link = localsite + '?filename1=' + File1Name + '&listfile=' + dataname[i] + '&id=' + dataid
        dicttmp['link'] = link
        tmp = dicttmp

        list.append(tmp)

    html_message = render_to_string('mail_template.html', {'data': list})
    id = data['id']

    plain_message = strip_tags(html_message)

    mail.send_mail('Hello', plain_message, 'kaitouthuan@gmail.com', [user], html_message=html_message)


def sendExportMailV2(data, sessionId):
    localsite = 'http://localhost:4200/daovan/' + str(sessionId)
    print(data)
    linkfile = os.getcwd() + '/MailComponent/mail_template2.html'

    print('user is')

    print('end')
    link = localsite

    html_message = render_to_string('mail_template2.html', {'link': link})
    print(html_message)
    id = data['id']
    user = User.objects.get(id=id)
    plain_message = strip_tags(html_message)

    mail.send_mail('Hello', plain_message, 'kaitouthuan@gmail.com', [user], html_message=html_message)
