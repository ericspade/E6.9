from django.shortcuts import render
from .models import Chat, Msg
from django.contrib.auth.decorators import login_required


@login_required
def chats(request):
    chats = Chat.objects.all()

    return render(request, 'chatrooms/chats.html', {'chats': chats})



@login_required
def chatroom(request, slug):
    chat = Chat.objects.get(slug=slug)
    messages = Msg.objects.filter(room=chat)

    return render(request, 'chatrooms/chat.html', {'chat': chat, 'messages': messages})
