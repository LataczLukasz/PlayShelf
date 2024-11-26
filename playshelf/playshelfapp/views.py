from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .models import Game

def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'playshelfapp/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'playshelfapp/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'playshelfapp/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def games_list(request):
    games = Game.objects.all()
    return render(request, 'playshelfapp/games_list.html', {'games': games})