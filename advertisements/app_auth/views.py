from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .forms import ExtendedUsercreationForm

@login_required(login_url=reverse_lazy('login'))
def profile_view(request):
    return render(request, 'app_auth/profile.html')

def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('profile'))
        return render(request, 'app_auth/login.html')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('profile'))
    return render(request, 'app_auth/login.html', {'error' : 'Пользователь не найден'})

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def register_views(request):
    if request.method == 'POST':
        form = ExtendedUsercreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=request.POST['password1'])
            login(request, user=user)
            return redirect(reverse('profile'))
    else:
        form = ExtendedUsercreationForm()

    context = {
        'form': form
    }
    return render (request, 'app_auth/register.html', context)




