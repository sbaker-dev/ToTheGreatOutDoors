from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from django.http import HttpResponse

from.models import Boundary, TravelLocation, RasterMap

# Create your views here.


def login_page(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username OR password is invalid")

    context = {'page': page}
    return render(request, 'pages/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user information temporarly so we can edit the stuff the user submits
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    context = {'form': form}
    return render(request, 'pages/login.html', context)


def home(request):

    return render(request, 'pages/home.html')


def select_location(request):

    # Isolate the unique categories
    categories = TravelLocation.objects.all().values("category").distinct()
    categories = [cat['category'] for cat in categories]

    context = {"locations_list": Boundary.objects.all(), "categories_list": categories,
               'raster_list': RasterMap.objects.all()}
    return render(request, 'pages/select_location.html', context=context)


def county(request, pk, place_type):

    travel_locations = TravelLocation.objects.filter(
        Q(category=place_type) &
        Q(place=pk)
    )

    context = {"locations_list": Boundary.objects.filter(place=pk), 'raster_list': RasterMap.objects.all(),
               'travel_locations': travel_locations}
    return render(request, 'pages/location.html', context)

