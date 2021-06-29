from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path

# from FileComponent import views
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from ExportResultComponent import views

urlpatterns = [
    # url(r'^test2', views.documentimportTesting),
    url(r"^export-result", csrf_exempt(views.ExportResult)),
    # url(r'^', include('UserComponent.urls')),
    # url(r'^$', views.home, name='home'),
    # url(r'^uploads/simple/$', views.simple_upload, name='simple_upload'),
    # url(r'^uploads/form/$', views.model_form_upload, name='model_form_upload'),
    # url(r'^admin/', admin.site.urls),
]
