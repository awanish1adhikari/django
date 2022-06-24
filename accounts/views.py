from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .auth import unauthenticated_user
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.auth import user_only
from .models import *
from .forms import *


@unauthenticated_user
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user,
                                   username=user.username)
            messages.add_message(request, messages.SUCCESS, 'User Registered Successfully')
            return redirect('/account')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to register user')
            return render(request, 'accounts/register.html', {'form': form})
    context = {
        'form': UserCreationForm
    }
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'],
                                password=data['password'])
            if user is not None:
                if not user.is_staff:
                    login(request, user)
                    return redirect('/')
                elif user.is_staff:
                    login(request, user)
                    return redirect('/admin')
            else:
                messages.add_message(request, messages.ERROR, 'Username or Password Invalid')
                return render(request, 'accounts/login.html', {'form': form})
    context = {
        'form': LoginForm
    }

    return render(request, 'accounts/login.html', context)


@login_required
@user_only
def user_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Update Successful for ' + str(request.user.profile.username))
            return redirect('/account/profile')
    context = {'form': form}
    return render(request, 'accounts/profile.html', context)


def logout_user(request):
    logout(request)
    return redirect('/')