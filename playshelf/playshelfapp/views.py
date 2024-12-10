from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from .models import Game

def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'playshelfapp/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )

def contact(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'playshelfapp/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )

def about(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'playshelfapp/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )

def games_list(request):
    games = Game.objects.all()
    if request.headers.get('Accept') == 'application/json':
        games_data = [
            {
                'title': game.title,
                'developer': game.developer,
                'publisher': game.publisher,
                'release_date': game.release_date.strftime('%Y-%m-%d'),
                'average_rating': game.average_rating,
                'description': game.description,
            }
            for game in games
        ]
        return JsonResponse({'games': games_data})
    return render(request, 'playshelfapp/games_list.html', {'games': games})
