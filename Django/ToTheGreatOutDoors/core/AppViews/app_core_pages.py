from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from ..models import Boundary, TravelLocation, RasterMap, Comment, Favorite


def home(request):
    """Home page"""
    return render(request, 'pages/home.html')


def select_location(request, state):
    """
    Isolate the unique categories names, and all the location, and raster maps to allow people to search for travel
    location within a given area
    """
    # Isolate the unique categories
    categories = TravelLocation.objects.all().values("category").distinct()
    categories = [cat['category'] for cat in categories]

    context = {"locations_list": Boundary.objects.all(), "categories_list": categories,
               'raster_list': RasterMap.objects.all(), 'state': state}
    return render(request, 'pages/select_location.html', context=context)


# TODO: Rename to travel location
def county(request, pk, place_type):
    """For a given boundary, find all the TravelLocations in that area that match that place type"""
    # Locations within this location of type 'place_type'
    travel_locations = TravelLocation.objects.filter(
        Q(category=place_type) &
        Q(place=pk)
    )

    if len(travel_locations) == 0:
        return redirect('select_location', "1")

    context = {"locations_list": Boundary.objects.filter(place=pk), 'raster_list': RasterMap.objects.all(),
               'travel_locations': travel_locations}
    return render(request, 'pages/location.html', context)


def place(request, place_name, place_location):
    """Get a given TravelLocation for viewing information. Allow individuals to add comment and select as favourites"""
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
            print("HERE?")
            Comment.objects.create(user=request.user,
                                   location=location,
                                   body=request.POST.get('body'),
                                   comment_group=len(comment_list))
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

        elif 'reply' in request.POST:
            print(request.POST.get('body'))
            print("Hello")
            print(request.POST.get('id'))
            original_comment = Comment.objects.get(id=request.POST.get('id'))

            reply = Comment.objects.create(user=request.user, location=location, body=request.POST.get('body'),
                                           comment_level=original_comment.comment_level + 1,
                                           comment_group=original_comment.comment_group)


            # Reply.objects.create(user=request.user, body=request.POST.get('body'))
            return redirect('place', place_name=place_name, place_location=place_location)

        else:
            print(f"Found unexpected POST command of {request.POST}")

    base_comments = [comment for comment in comment_list if comment.comment_level == 0]
    replies = [comment for comment in comment_list if comment.comment_level > 0]


    context = {'comment_list': base_comments, 'location': location, 'favourite': len(fav_list) == 1, 'replies': replies}
    return render(request, 'pages/place_details.html', context)


def search_location(request):
    """
    Instead of using map views, use the search bar. Default state is that nothing has been searched, but if
    POST, then actually try to find locations that match or contains the searchName
    """
    context = {'matchLocation': [], 'searchStatus': 0, 'matchLength': 0, 'searchName': ""}
    if request.method == 'POST':

        context['matchLocation'] = TravelLocation.objects.filter(name__contains=request.POST.get('searchName'))
        context['searchStatus'] = 1
        context['matchLength'] = len(context['matchLocation'])
        context['searchName'] = request.POST.get('searchName')

    return render(request, 'pages/search_location.html', context)


def contact(request):
    """Basic contact page"""
    return render(request, 'pages/contact.html')
