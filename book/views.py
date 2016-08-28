from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data.get('username'),
                        first_name=form.cleaned_data.get('first_name'),
                        last_name=form.cleaned_data.get('last_name'),
                        email=form.cleaned_data.get('email'),
                        password=make_password(form.cleaned_data.get('password')))
            user.save()
            userprofile = UserProfile(user_id=user,
                                      city=form.cleaned_data.get('city'),
                                      country=form.cleaned_data.get('country'),
                                      date_of_birth=form.cleaned_data.get('date_of_birth'),
                                      description=form.cleaned_data.get('description'))
            userprofile.save()
            messages.add_message(request, messages.INFO, 'You have been registered. You can now log in.')
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
        messages.add_message(request, messages.ERROR, '*Invalid credentials')
        return redirect('register')


def logout_view(request):
    logout(request)
    return redirect('register')


@login_required
def home_page(request):
    return render(request, 'book/home_page.html', {})


@login_required
def edit_profile(request):
    user = request.user
    profile = request.user.userprofile
    form = SignUpForm(initial={'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name,
                               'email': user.email, 'city': profile.city, 'country': profile.country,
                               'date_of_birth': profile.date_of_birth, 'description': profile.description})
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data.get('username')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.password = make_password(form.cleaned_data.get('password'))
            user.save()
            profile.user_id = user
            profile.city = form.cleaned_data.get('city')
            profile.country = form.cleaned_data.get('country')
            profile.date_of_birth = form.cleaned_data.get('date_of_birth')
            profile.description = form.cleaned_data.get('description')
            profile.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.INFO, 'Your personal data has been saved.')
    return render(request, 'book/edit_profile.html', {'form': form})
