import json
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Msg
from asgiref.sync import sync_to_async


class Member(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        self.chat_group_name = self.chat_name

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)
        msg = data['msg']
        username = data['username']
        chat = data['chatname']

        await self.save_msg(username, chat, msg)

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'msg': msg,
                'username': username,
                'chat': chat,
            }
        )

    async def chat_message(self, event):
        msg = event['msg']
        username = event['username']
        chat = event['chat']

        await self.send(text_data=json.dumps({
            'msg': msg,
            'username': username,
            'chat': chat,
        }))

    @sync_to_async
    def save_msg(self, username, chat, msg):
        user = User.objects.get(username=username)
        chat = Chat.objects.get(slug=chat)

        Msg.objects.create(user=user, room=chat, text=msg)
