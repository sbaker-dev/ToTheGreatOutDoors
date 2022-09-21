from django.shortcuts import render


def contact(request):
    """Basic contact page"""
    return render(request, 'pages/contact.html')
