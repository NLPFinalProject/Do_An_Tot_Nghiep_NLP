from django.conf.urls import url 
from UserComponent import views 
from django.urls import include, path
urlpatterns = [ 
    
     url(r'^customers/$', views.customer_list),
     url(r'^customers/(?P<pk>[0-9]+)$', views.customer_detail),
     url(r'^customers/age/(?P<age>[0-9]+)/$', views.customer_list_age),
     url(r'^api/login',views.login),
     url(r'^api/reset-password',views.ResetPassword),
     url(r'^api/forgot-password',views.ForgetPassword),
     url(r'^api/SendMail',views.SendEmail),
     url(r'^api/activate',views.ActivateUser),
     url(r'^activate',views.ActivateUser),
     url(r'^SendMail',views.SendEmail),
     #path(r'^SendMail',include('allauth.urls')),
     url('api/SendMail',views.SendEmail),
     url('register',views.SendEmail),
     path('api-auth/', include('rest_framework.urls')),

     
     #url('api/register',views.SendEmail),
]
