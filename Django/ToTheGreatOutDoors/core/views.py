from django.shortcuts import render
from django.http import HttpResponse

from.models import Boundary, Location

# Create your views here.


def home(request):

    # Isolate the unique categories
    categories = Location.objects.all().values("category").distinct()


    context = {"locations_list": Boundary.objects.all(), "categories_list": categories}
    return render(request, 'home.html', context=context)



