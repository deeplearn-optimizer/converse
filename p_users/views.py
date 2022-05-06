import profile
from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf
from django.http import JsonResponse

from projects.models import Query
from django.db.models import Q
from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, MessageForm
from .utils import searchProfiles, paginateProfiles

from p_users.models import Profile
from rest_framework import serializers

import logging
logger = logging.getLogger(__name__)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

def get_profiles(request = None):
    users = Profile.objects.all()
    serializer = ProfileSerializer(users, many=True)
    return JsonResponse(serializer.data, safe = False)


def loginUser(request):
    logger.info("user login page was accessed!")
    page = 'login'

    if request.user.is_authenticated:
        return redirect('account')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            logger.info("User logged in.")
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            logger.warning("User cannot log in.")
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'p_users/login_register.html')
    

def logoutUser(request):
    logger.info("user logged out")
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login') 



def registerUser(request):
    logger.info("Trying to register new user.")
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            logger.info("User registered.")
            login(request, user)
            return redirect('edit-account')

        else:
            messages.error(
                request, 'An error has occurred during registration')
            logger.error("cannot register user")

    context = {'page': page, 'form': form}
    return render(request, 'p_users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 3)
    context = {'profiles': profiles, 'search_query': search_query,
               'custom_range': custom_range}
    return render(request, 'p_users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    queries =  profile.query_set.all();
    context = {'profile': profile, "queries" : queries}
    return render(request, 'p_users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    logger.info("user account accessed.")
    profile = request.user.profile
    queries =  profile.query_set.all();
    context = {'profile': profile, "queries" : queries}
    return render(request, 'p_users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    logger.info("account edit was accessed.")
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'p_users/profile_form.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'p_users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    logger.info("message was shown.")
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'p_users/message.html', context)

def createMessage(request, pk):
    logger.info("message was created.")
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'p_users/message_form.html', context)


