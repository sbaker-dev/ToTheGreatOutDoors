from django.shortcuts import render
from django.db.models import Q

from ..models import Comment, Favorite


def account_page(request):
    """The account page contains all the favourites, messages, and replies from other users, that have been made"""
    user_favourites = Favorite.objects.filter(user=request.user)
    user_messages = Comment.objects.filter(user=request.user)
    reply_messages = Comment.objects.filter(Q(comment_level__gt=0) & ~Q(user=request.user))

    context = {'userDetails': request.user, 'favourites': user_favourites, 'comment_list': user_messages,
               'reply_list': reply_messages}
    return render(request, 'pages/account.html', context)
