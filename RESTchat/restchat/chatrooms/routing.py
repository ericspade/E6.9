from django.urls import path
from . import members

websocket_urlpatterns = [
    path('ws/<str:chat_name>/', members.Member.as_asgi()),
]