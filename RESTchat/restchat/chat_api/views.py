import json

from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from .serializer import DataSerializer, ChangePasswordSerializer, UserSerializers
from chatrooms.models import Chat
from django.contrib.auth.models import User


@login_required
@api_view(['GET'])
def getChats(request):
    chats = Chat.objects.all()
    serializer = DataSerializer(chats, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createChats(request):
    serializer = DataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)

    return redirect('chats')


@api_view(['GET', 'DELETE'])
def deleteChat(request, slug):
    Chat.objects.get(slug=slug).delete()
    return redirect('chats')


@api_view(['POST'])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Пароль изменен!'}, status=status.HTTP_200_OK)
            return Response({'error': 'Неверный текущий пароль.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def changeusername(request):
    user = request.user
    serializer = UserSerializers(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        chat = Chat.objects.get(name=user.username)
        serializer.save()
        chat.name = user.username
        chat.slug = user.username
        chat.save()
        return Response(serializer.data)
