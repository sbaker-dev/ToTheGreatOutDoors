from django.shortcuts import render, redirect
from django.db.models import Q

from ..models import Boundary, TravelLocation, RasterMap


def travel_location(request, pk, place_type):
    """
    For a given district, find all the TravelLocations in that area that match that place type. If they find no
    destinations of place_type at this location, then redirect to select location
    """
    # Locations within this location of type 'place_type'
    travel_locations = TravelLocation.objects.filter(
        Q(category=place_type) &
        Q(place=pk)
    )

    # If we find no locations, return to select location with the error flag raised
    if len(travel_locations) == 0:
        return redirect('select_location', "1")

    context = {"locations_list": Boundary.objects.filter(place=pk), 'raster_list': RasterMap.objects.all(),
               'travel_locations': travel_locations}
    return render(request, 'pages/location.html', context)
