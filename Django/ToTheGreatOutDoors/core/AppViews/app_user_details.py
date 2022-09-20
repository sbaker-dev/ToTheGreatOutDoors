from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from django.http import HttpResponse
from django.db.models import Q

from ..models import Comment, Favorite


@csrf_protect
def login_page(request):
    """Login page"""
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username OR password is invalid")
            return redirect('login')

    context = {'page': page}
    return render(request, 'pages/login.html', context)


def logout_user(request):
    """Log out user"""
    logout(request)
    return redirect('home')


def register_user(request):
    """Register the user, if they have requested it"""
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user information temporarily so we can edit the stuff the user submits
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    context = {'form': form}
    return render(request, 'pages/login.html', context)


@login_required(login_url='loginPage')
def delete_message(request, pk):
    """Delete a message"""
    message_to_delete = Comment.objects.get(id=pk)
    if request.user != message_to_delete.user:
        return HttpResponse("You are not allowed here")

    if request.method == 'POST':
        message_to_delete.delete()
        # TODO: This should link to account page
        return redirect('home')
    return render(request, 'pages/delete_comment.html', {'obj': message_to_delete})


def account_page(request):
    """The account page contains all the favourites and messages that user made"""
    user_favourites = Favorite.objects.filter(user=request.user)
    user_messages = Comment.objects.filter(user=request.user)
    reply_messages = Comment.objects.filter(Q(comment_level__gt=0) & ~Q(user=request.user))



    print(reply_messages)

    context = {'userDetails': request.user, 'favourites': user_favourites, 'comment_list': user_messages}
    return render(request, 'pages/account.html', context)