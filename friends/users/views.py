from users.models import MyUser, FriendRequest
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import authenticate
from users.forms import UserCreationForm


class Register(View):
    """ Регистрация пользователя """
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def home_page(request):
    """ Домашнаяя страница """
    all_users = MyUser.objects.exclude(username=request.user)
    incoming = FriendRequest.objects.filter(recipient=request.user)
    outcoming = FriendRequest.objects.filter(sender=request.user)
    return render(request, 'home.html', {'all_users': all_users, 'incoming': incoming, 'outcoming': outcoming})


def send_request(request, id):
    """ Отправка запроса в друзья """
    sender = request.user
    recipient = MyUser.objects.get(id=id)
    frequest = FriendRequest.objects.get_or_create(sender=sender, recipient=recipient)
    return redirect('home')


def accept_request(request, id):
    """ Принять зявку в друзья """
    frequset = FriendRequest.objects.get(id=id)
    user1 = request.user
    user2 = frequset.sender
    user1.friends.add(user2)
    user2.friends.add(user1)
    return redirect('home')


def reject_request(request, id):
    """ Отклонить заявку в друзья """
    frequest = FriendRequest.objects.get(id=id)
    user1 = request.user
    user2 = frequest.sender
    user1.friends.remove(user2)
    user2.friends.remove(user1)
    return redirect('home')
