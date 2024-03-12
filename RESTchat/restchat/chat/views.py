from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from chatrooms.models import Chat, Msg


def title(request):
    return render(request, 'common/main.html')


def signupform(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('title page')

    else:
        form = SignUpForm()

    return render(request, 'common/signup.html', {'form': form})


@login_required
def users(request):
    users = User.objects.all()
    return render(request, 'chatrooms/users.html', {'users': users})


@login_required
def sendmessage(request, usernameX):
    user = User.objects.get(username=usernameX)
    json = {
        'name': user.username,
        'slug': user.username,
    }
    chat = Chat.objects.create(**json)
    messages = Msg.objects.filter(room=chat)
    return render(request, 'chatrooms/users.html', {'usernameX': usernameX})


@login_required
def userchats(request):
    chats = Chat.objects.filter(owner=request.user.username)

    return render(request, 'chatrooms/userchats.html', {'chats': chats})