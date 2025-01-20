from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from .models import Game, Review, User
from .serializers import GameSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .serializers import CustomTokenObtainPairSerializer, UserRegistrationSerializer, ReviewSerializer

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


class GameList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
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
    
    
class GameRatingsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, game_id):
        user = request.user  # Uzyskujemy dane użytkownika
        game = Game.objects.filter(game_id=game_id).first()  # Pobieramy grę na podstawie game_id
        
        if not game:
            return Response({'error': 'Gra nie została znaleziona'}, status=404)
        
        reviews = Review.objects.filter(game=game)
        my_review = reviews.filter(user=user).first()
        
        reviews_to_serialize = reviews.exclude(review_id=my_review.review_id) if my_review else reviews
        review_serializer = ReviewSerializer(reviews_to_serialize, many=True)
        
        my_review_data = ReviewSerializer(my_review).data if my_review else None

        return Response({
            'reviews': review_serializer.data,
            'my_review': my_review_data,
            'game': game.title,
            'game_id': game.game_id,
        })

    
class GameRatingsEditView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        game_id = data.get('game_id')
        game = Game.objects.filter(game_id=game_id).first()

        if not game:
            return Response({'error': 'Gra nie została znaleziona'}, status=status.HTTP_404_NOT_FOUND)

        existing_review = Review.objects.filter(user=user, game=game).first()

        if existing_review:
            existing_review.review_text = data.get('review_text', existing_review.review_text)
            existing_review.rating = data.get('rating', existing_review.rating)
            existing_review.review_date = datetime.now().date()
            existing_review.save()
            serializer = ReviewSerializer(existing_review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = ReviewSerializer(data={
                'review_date': datetime.now().date(),
                'review_text': data.get('review_text'),
                'rating': data.get('rating'),
            })
            if serializer.is_valid():
                serializer.save(user=user, game=game)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)