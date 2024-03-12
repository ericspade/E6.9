from django.urls import path
from . import views

urlpatterns = [
    path('', views.getChats),
    path('post/', views.createChats),
    path('delete/<slug:slug>', views.deleteChat, name='delete chat'),
    path('changepassword/', views.change_password, name='change_password'),
    path('changeusername/', views.changeusername, name='changeusername'),
]
