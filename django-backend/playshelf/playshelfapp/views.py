from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from .models import Game
from .serializers import GameSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


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

@api_view(['GET'])
def games_list(request):
    games = Game.objects.all()
    if request.headers.get('Accept') == 'application/json':
        serializer = GameSerializer(games, many=True)
        return Response({'games': serializer.data})
    return render(request, 'playshelfapp/games_list.html', {'games': games})

