from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_user(request):
    """Log out user"""
    logout(request)
    return redirect('home')
