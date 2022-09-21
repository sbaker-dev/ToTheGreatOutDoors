from django.shortcuts import render

from ..models import TravelLocation


def search_location(request):
    """
    Instead of using map views, use the search bar. Default state is that nothing has been searched, but if
    POST, then actually try to find locations that match or contains the searchName
    """
    context = {'matchLocation': [], 'searchStatus': 0, 'matchLength': 0, 'searchName': ""}
    if request.method == 'POST':
        context['matchLocation'] = TravelLocation.objects.filter(name__icontains=request.POST.get('searchName'))
        context['searchStatus'] = 1
        context['matchLength'] = len(context['matchLocation'])
        context['searchName'] = request.POST.get('searchName')

    return render(request, 'pages/search_location.html', context)