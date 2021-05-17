from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from FileComponent import views
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # url(r'^test2', views.documentimportTesting),
    url(r'^checkdatabase', csrf_exempt(views.documentimportDatabase)),
    url(r'^final-check', csrf_exempt(views.FinalCheck)),
    url(r'^checkinternet', csrf_exempt(views.documentimportInternet)),
    url(r'^test3', csrf_exempt(views.documentimport)),
    url(r'^test2', csrf_exempt(views.ff)),
    url(r'^test', views.test),
    url(r'^uploadfilelist', csrf_exempt(views.uploadDocList)),
    url(r'^uploadfile', csrf_exempt(views.uploadDoc)),

    # url(r'^', include('UserComponent.urls')),
    # url(r'^$', views.home, name='home'),
    # url(r'^uploads/simple/$', views.simple_upload, name='simple_upload'),
    # url(r'^uploads/form/$', views.model_form_upload, name='model_form_upload'),
    # url(r'^admin/', admin.site.urls),
]