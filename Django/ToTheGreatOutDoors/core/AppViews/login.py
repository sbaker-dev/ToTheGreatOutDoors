from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


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