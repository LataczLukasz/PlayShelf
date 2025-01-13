from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from .models import Game
from .serializers import GameSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .serializers import CustomTokenObtainPairSerializer, UserRegistrationSerializer

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

class GameList(APIView):
    permission_classes = []
    def get(self, request):
        print(request.user.id)
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response({'games': serializer.data})


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = []
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        # Sprawdź, czy dane są poprawne
        if serializer.is_valid():
            # Jeśli dane są poprawne, zwróć tokeny w formacie JSON
            return Response({
                'message': 'Zalogowano pomyślnie',
                'access_token': serializer.validated_data['access'],
                'refresh_token': serializer.validated_data['refresh']
            }, status=status.HTTP_200_OK)
        else:
            # W przypadku błędów zwróć komunikat z błędami
            return Response({
                'message': 'Nie udało się zalogować',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Wylogowano pomyślnie."}, status=200)
        return response

class UserRegistrationView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Tworzenie użytkownika
            return Response({
                "message": "Rejestracja przebiegła pomyślnie.",
                "user": {
                    "id": user.user_id,
                    "email": user.email,
                    "username": user.username,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)