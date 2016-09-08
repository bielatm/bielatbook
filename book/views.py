from django.shortcuts import render, redirect
from .forms import SignUpForm, UserProfileForm
from django.contrib.auth.models import User
from .models import UserProfile, FriendshipInvite, Friendship, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    form = UserProfileForm(initial={'first_name': user.first_name,
                                    'last_name': user.last_name, 'email': user.email,
                                    'city': profile.city, 'country': profile.country,
                                    'date_of_birth': profile.date_of_birth, 'description': profile.description})
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user.username = user.username
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


@login_required
def find_friends(request):
    user = request.user
    invited_users_ids = [f.friend_id for f in user.sent_friendship_invites.all()]
    friends_ids = [f.user_id for f in user.friendships.all()]
    uninvited_users = User.objects.filter(~Q(id__in=invited_users_ids + [request.user.id] + friends_ids),
                                          is_superuser=False).order_by('first_name')
    paginator = Paginator(uninvited_users, 3)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        friendship = FriendshipInvite(user_id=user.id, friend_id=request.POST['friend_id'])
        friendship.save()
        friend = User.objects.get(id=request.POST['friend_id'])
        messages.add_message(request, messages.INFO, 'You added ' + friend.first_name + ' '
                             + friend.last_name + ' to your friends.')
        return redirect('find_friends')
    return render(request, 'book/find_friends.html', {'users': users})


@login_required
def accept_invitations(request):
    user = request.user
    received_invitations = user.received_friendship_invites.all()
    paginator = Paginator(received_invitations, 3)
    page = request.GET.get('page')
    try:
        invitations = paginator.page(page)
    except PageNotAnInteger:
        invitations = paginator.page(1)
    except EmptyPage:
        invitations = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        friendship = FriendshipInvite.objects.get(id=request.POST['friendship_id'])
        Friendship(user=friendship.user, friend=friendship.friend).save()
        Friendship(user=friendship.friend, friend=friendship.user).save()
        friendship.delete()
        return redirect('accept_invitations')
    return render(request, 'book/invitations.html', {'invitations': invitations})


@login_required
def friends_list(request):
    user = request.user
    buddys_list = [f.user for f in user.friendships.all()]
    buddys_list.sort(key=lambda x: x.first_name, reverse=False)
    paginator = Paginator(buddys_list, 3)
    page = request.GET.get('page')
    try:
        friends = paginator.page(page)
    except PageNotAnInteger:
        friends = paginator.page(1)
    except EmptyPage:
        friends = paginator.page(paginator.num_pages)
    return render(request, 'book/friends_list.html', {'friends': friends})


@login_required
def messages_list(request):
    user = request.user
    messages_from_friends = user.messages.all()
    return render(request, 'book/messages_list.html', {'messages_from_friends': messages_from_friends})
