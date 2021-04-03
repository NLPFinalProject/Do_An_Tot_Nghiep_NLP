from django.contrib import admin
from django.conf.urls import url, include 
from django.urls import path
from FileComponent import views
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    url(r'^test2', views.documentimport),
    url(r'^test', views.test),
   
<<<<<<< HEAD
    url(r'^uploadfile',csrf_exempt(views.uploadDoc))
    
=======
    url(r'^uploadfile',csrf_exempt(views.uploadDoc)),
    url(r'^uploadfilelist',csrf_exempt(views.uploadDoc)),
>>>>>>> branch-3--database
    #url(r'^', include('UserComponent.urls')), 
    #url(r'^$', views.home, name='home'),
   # url(r'^uploads/simple/$', views.simple_upload, name='simple_upload'),
    #url(r'^uploads/form/$', views.model_form_upload, name='model_form_upload'),
    #url(r'^admin/', admin.site.urls),
]