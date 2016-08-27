from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = form.cleaned_data.get('username')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.password = make_password(form.cleaned_data.get('password'))
            user.save()
            userprofile = UserProfile()
            userprofile.user_id = user
            userprofile.city = form.cleaned_data.get('city')
            userprofile.country = form.cleaned_data.get('country')
            userprofile.date_of_birth = form.cleaned_data.get('date_of_birth')
            userprofile.description = form.cleaned_data.get('description')
            userprofile.save()
            return redirect('register')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration.html', {'form': form})


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return redirect('home_page')
    else:
        messages.add_message(request, messages.INFO, '*Invalid credentials')
        return redirect('register')


def logout_view(request):
    logout(request)
    return redirect('register')


@login_required
def home_page(request):
    return render(request, 'book/home_page.html', {})


@login_required
def edit_profile(request):
    profile = request.user
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            profile = form.save()
            profile.save()
            print(profile.city)
            return redirect('home_page')
    else:
        form = SignUpForm()
    return render(request, 'book/edit_profile.html', {'form': form})
