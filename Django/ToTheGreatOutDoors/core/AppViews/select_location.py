from django.shortcuts import render

from ..models import Boundary, TravelLocation, RasterMap


def select_location(request, state):
    """
    Isolate the unique categories names, all the districts, and the raster maps to allow people to select an area they
    wish to search for a destination.

    State is designed to handle redirections. If we travel to the page directly, the state is zero. However, if the user
    selects a category that has no locations within that place, then we return to this location with a state of 1, which
    will raise an error message.
    """
    # Isolate the unique categories
    categories = TravelLocation.objects.all().values("category").distinct()
    categories = [cat['category'] for cat in categories]

    context = {"locations_list": Boundary.objects.all(), "categories_list": categories,
               'raster_list': RasterMap.objects.all(), 'state': state}
    return render(request, 'pages/select_location.html', context=context)