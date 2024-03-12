from django.urls import path
from django.contrib.auth import views as sign_views

from . import views


urlpatterns = [
    path('', views.title, name='title page'),
    path('signup/', views.signupform, name='signup'),
    path('signin/', sign_views.LoginView.as_view(template_name='common/signin.html'), name='signin'),
    path('signout/', sign_views.LogoutView.as_view(), name='signout'),
    path('users/', views.users, name='users'),
    path('sendmessage/', views.sendmessage, name='sendmessage'),
    path('userchats/', views.userchats, name='userchats'),
]
