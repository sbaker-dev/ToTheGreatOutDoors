from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from ..models import Comment


@login_required(login_url='loginPage')
def delete_message(request, pk):
    """Delete a message"""
    message_to_delete = Comment.objects.get(id=pk)
    if request.user != message_to_delete.user:
        return HttpResponse("You are not allowed here")

    if request.method == 'POST':
        message_to_delete.delete()
        return redirect('accountPage')
    return render(request, 'pages/delete_comment.html', {'obj': message_to_delete})
