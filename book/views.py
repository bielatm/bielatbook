from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, UserProfileForm, MessageForm, InputMessageForm, GroupForm
from django.contrib.auth.models import User
from .models import UserProfile, FriendshipInvite, Friendship, Message, Group, Post, Membership
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain


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
    messages_from_friends = user.received_messages.order_by('author', '-created_at').distinct('author')
    messages_from_friends = sorted(messages_from_friends, key=lambda x: x.created_at, reverse=True)
    return render(request, 'book/messages_list.html', {'messages_from_friends': messages_from_friends})


@login_required
def new_message(request):
    user = request.user
    friends = [f.user for f in user.friendships.all()]
    if request.method == 'POST':
        form = MessageForm(request.POST, receiver_ids=[(f.id, '{0} {1}'.format(f.first_name, f.last_name)) for f in friends])
        if form.is_valid():
            message = Message(author=user,
                              text=form.cleaned_data.get('text'),
                              receiver_id=form.cleaned_data.get('receiver_id'))
            message.save()
            messages.add_message(request, messages.INFO, 'Your message has been sent.')
            return redirect('new_message')
    else:
        form = MessageForm(receiver_ids=[(f.id, '{0} {1}'.format(f.first_name, f.last_name)) for f in friends])
    return render(request, 'book/new_message.html', {'form': form, 'friends': friends})


@login_required
def friend_messages(request, pk):
    user = request.user
    friend = get_object_or_404(User, pk=pk)
    received_messages = user.received_messages.filter(author=friend)
    sent_messages = user.sent_messages.filter(receiver=friend)
    all_messages = sorted(list(chain(received_messages, sent_messages)), key=lambda x: x.created_at, reverse=True)
    if request.method == 'POST':
        form = InputMessageForm(request.POST)
        if form.is_valid():
            # message = Message(author=user,
            #                   text=form.cleaned_data.get('text'),
            #                   receiver=friend)
            message = form.save(commit=False)
            message.author = user
            message.receiver = friend
            message.save()
            return redirect('friend_messages', pk=friend.pk)
    else:
        form = InputMessageForm()
    return render(request, 'book/friend_messages.html', {'all_messages': all_messages, 'friend': friend, 'form': form})


@login_required
def groups_list(request):
    groups = [g.group for g in request.user.group_memberships.all()]
    return render(request, 'book/groups_list.html', {'groups': groups})


@login_required
def new_group(request):
    user = request.user
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.admin = user
            group.save()
            membership = Membership(group_id=group.id, user_id=user.id)
            membership.save()
            return redirect('groups_list')
    else:
        form = GroupForm()
    return render(request, 'book/new_group.html', {'form': form})


@login_required
def group_detail(request, pk):
    user = request.user
    group = get_object_or_404(Group, pk=pk)
    members = [u.user for u in group.user_memberships.all()]
    if user not in members:
        return redirect('groups_list')
    return render(request, 'book/group_detail.html', {'group': group, 'user': user})


@login_required
def group_remove(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if group.admin == request.user:
        group.delete()
    return redirect('book.views.groups_list')


@login_required
def add_members(request, pk):
    user = request.user
    group = get_object_or_404(Group, pk=pk)
    friends = [f.user for f in user.friendships.all()]
    friends.sort(key=lambda x: x.first_name, reverse=False)
    members = [u.user for u in group.user_memberships.all()]
    uninvited_friends = list(set(friends)-set(members))
    uninvited_friends.sort(key=lambda x: x.first_name, reverse=False)
    if user not in members:
        return redirect('groups_list')
    if request.method == 'POST':
        membership = Membership(group_id=group.id, user_id=request.POST['friend_id'])
        membership.save()
        return redirect('add_members', pk=group.pk)
    return render(request, 'book/add_members.html', {'friends': uninvited_friends, 'group': group, 'user': user})
