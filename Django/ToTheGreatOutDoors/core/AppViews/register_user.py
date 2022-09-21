from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


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
