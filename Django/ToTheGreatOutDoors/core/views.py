from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Boundary, TravelLocation, RasterMap, Comment, Favorite


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


# TODO: Rename to travel location
def county(request, pk, place_type):
    # Locations within this location of type 'place_type'
    travel_locations = TravelLocation.objects.filter(
        Q(category=place_type) &
        Q(place=pk)
    )

    context = {"locations_list": Boundary.objects.filter(place=pk), 'raster_list': RasterMap.objects.all(),
               'travel_locations': travel_locations}
    return render(request, 'pages/location.html', context)


def place(request, place_name, place_location):
    location = TravelLocation.objects.filter(Q(name=place_name) &
                                             Q(place=place_location))

    # TODO: we probably also need to store GID, and filter on this, as locations can have names within the same location
    if len(location) > 1:
        print("Warning, found multiple locations within the same name in the same location (shouldn't be possible)")
    location = location[0]
    comment_list = location.comment_set.all().order_by('-created')

    if request.user.is_authenticated:
        fav_list = Favorite.objects.filter(Q(user=request.user) & Q(location=location))
    else:
        fav_list = []

    if request.method == "POST":
        # New comment has been posted, update.
        if 'comment' in request.POST:
            Comment.objects.create(user=request.user,
                                   location=location,
                                   body=request.POST.get('body'))
            return redirect('place', place_name=place_name, place_location=place_location)

        elif 'favourite' in request.POST:

            # If it was a favourite, un-favourite it
            try:
                Favorite.objects.get(user=request.user, location=location).delete()
                print("Removing fav")
                return redirect('place', place_name=place_name, place_location=place_location)

            # Otherwise, add it as a fav
            except ObjectDoesNotExist:
                print("Adding Fav")
                Favorite.objects.create(user=request.user, location=location)
                return redirect('place', place_name=place_name, place_location=place_location)

        else:
            print(f"Found unexpected POST command of {request.POST}")

    context = {'comment_list': comment_list, 'location': location, 'favourite': len(fav_list) == 1}
    return render(request, 'pages/place_details.html', context)


@login_required(login_url='loginPage')
def delete_message(request, pk):
    message_to_delete = Comment.objects.get(id=pk)
    if request.user != message_to_delete.user:
        return HttpResponse("You are not allowed here")

    if request.method == 'POST':
        message_to_delete.delete()
        # TODO: This should link to account page
        return redirect('home')
    return render(request, 'components/user/delete_comment.html', {'obj': message_to_delete})


def account_page(request):

    user_favourites = Favorite.objects.filter(user=request.user)
    user_messages = Comment.objects.filter(user=request.user)

    context = {'userDetails': request.user, 'favourites': user_favourites, 'comment_list': user_messages}
    return render(request, 'pages/account.html', context)


def search_location(request):
    context = {'matchLocation': [], 'searchStatus': 0, 'matchLength': 0, 'searchName': ""}
    if request.method == 'POST':

        context['matchLocation'] = TravelLocation.objects.filter(name__contains=request.POST.get('searchName'))
        context['searchStatus'] = 1
        context['matchLength'] = len(context['matchLocation'])
        context['searchName'] = request.POST.get('searchName')

    return render(request, 'pages/search_location.html', context)


def contact(request):
    return render(request, 'pages/contact.html')
