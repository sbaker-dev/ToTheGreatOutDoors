from django.shortcuts import render
from django.http import HttpResponse

from.models import Boundary, TravelLocation

# Create your views here.


def home(request):

    # Isolate the unique categories
    categories = TravelLocation.objects.all().values("category").distinct()
    categories = [cat['category'] for cat in categories]

    print(categories)

    context = {"locations_list": Boundary.objects.all(), "categories_list": categories}
    return render(request, 'home.html', context=context)



