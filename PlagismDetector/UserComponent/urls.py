from django.conf.urls import url 
from UserComponent import views 
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
urlpatterns = [ 
     #path('auth/', include('rest_auth.urls')),
     
     #url(r'^api/login', csrf_exempt(TokenObtainPairView.as_view())),
     #url(r'^login', TokenObtainPairView.as_view()),
     #url(r'^refresh-token/', TokenRefreshView.as_view()),
     #path('/profile',views.GetProfile),
     url(r'^api/SendMail',csrf_exempt(views.register)),
     url(r'register',csrf_exempt(views.register)),
     url(r'update-user',csrf_exempt(views.UpdateUser)),
     url(r'SendMail',csrf_exempt(views.register)),
     url(r'session',views.Session),
     url(r'get-user-list',csrf_exempt(views.UserList)),
     url(r'^profile',views.GetProfile),
     #url(r'^login',views.login),
     url(r'^login', views.NewAPILogin.as_view()),
     url(r'^is-admin-user', csrf_exempt(views.isAdmin)),
     url(r'^lock-user', csrf_exempt(views.lockUser)),
     url(r'^unlock-user', csrf_exempt(views.unlockUser)),
     url(r'^refresh-token/', refresh_jwt_token),
     path('api/refresh-token/', refresh_jwt_token),
     url(r'^reset-password',views.ResetPassword),
     url(r'^forgot-password',views.ForgetPassword),
     url(r'^api/register',csrf_exempt(views.register)),
     url(r'^api/activate',views.ActivateUser),
     url(r'^activate',views.ActivateUser),
     #path(r'^SendMail',include('allauth.urls')),
     #remove if not affected
     path('api/token/',TokenObtainPairView.as_view()),
     path('api/token/refresh/',TokenRefreshView.as_view()),
     path('api-auth/', include('rest_framework.urls')),

]
