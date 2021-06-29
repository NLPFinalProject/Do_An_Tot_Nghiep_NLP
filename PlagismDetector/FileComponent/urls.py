from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from FileComponent import views
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # url(r'^test2', views.documentimportTesting),
    url(r"^checkdatabaseinternet", csrf_exempt(views.documentimportDatabaseInternet)),
    url(r"^checkdatabase", csrf_exempt(views.documentimportDatabase)),
    url(r"^final-check", csrf_exempt(views.FinalCheck)),
    url(r"^uploadfilelist", csrf_exempt(views.uploadDocListRequest)),
    url(r"^checkinternet", csrf_exempt(views.documentimportInternet)),
    url(r"^getjsonresult", csrf_exempt(views.readJsonRequest)),
    # url(r'^checkdatabaseinternet', csrf_exempt(views.documentimportDatabaseInternet)),
    url(r"^test3", csrf_exempt(views.documentimport)),
    url(r"^test2", csrf_exempt(views.ff)),
    url(r"^test", views.test),
    # url(r'^uploadfilelist', csrf_exempt(views.uploadDocList2)),
    # url(r'^uploadfile', csrf_exempt(views.uploadDoc2)),
    # url(r'^', include('UserComponent.urls')),
    # url(r'^$', views.home, name='home'),
    # url(r'^uploads/simple/$', views.simple_upload, name='simple_upload'),
    # url(r'^uploads/form/$', views.model_form_upload, name='model_form_upload'),
    # url(r'^admin/', admin.site.urls),
]
