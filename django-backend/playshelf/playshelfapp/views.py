from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from .models import Game, Review, User, Wishlist, GameImage
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

def about(request):
    return render(request, 'playshelfapp/about.html', {
        'title': 'About Us',
        'message': 'This is the about page content.'
})

def contact(request):
    return render(request, 'playshelfapp/contact.html', {
        'title': 'Contact Us',
        'message': 'You can contact us at this email.'
})

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = []
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        

        if serializer.is_valid():

            return Response({
                'message': 'Zalogowano pomyślnie',
                'access_token': serializer.validated_data['access'],
                'refresh_token': serializer.validated_data['refresh']
            }, status=status.HTTP_200_OK)
        else:

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
            user = serializer.save() 
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
        user = request.user 
        game = Game.objects.filter(game_id=game_id).first()
        
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
        
class GameWishlistAddView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        data = request.data
        game_id = data.get('id')
        game = Game.objects.filter(game_id=game_id).first()

        if not game:
            return Response({'error': 'Gra nie została znaleziona'}, status=status.HTTP_404_NOT_FOUND)

        wishlist, created = Wishlist.objects.get_or_create(user=user, game=game)

        if created:
            return Response({'message': 'Gra została dodana do listy życzeń'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Gra już znajduje się na liście życzeń'}, status=status.HTTP_200_OK)
        
class GameWishlistRemoveView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        data = request.data
        game_id = data.get('id')
        game = Game.objects.filter(game_id=game_id).first()

        if not game:
            return Response({'error': 'Gra nie została znaleziona'}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item = Wishlist.objects.filter(user=user, game=game).first()

        if wishlist_item:
            wishlist_item.delete()
            return Response({'message': 'Gra została usunięta z listy życzeń'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Gra nie znajduje się na liście życzeń'}, status=status.HTTP_404_NOT_FOUND)

class GameWishlistView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        wishlist_items = Wishlist.objects.filter(user=user)
        games = [item.game for item in wishlist_items]
        serializer = GameSerializer(games, many=True)
        
        games_with_images = []
        for game in games:
            game_data = serializer.data[games.index(game)]
            game_image = GameImage.objects.filter(game=game).first()
            game_data['image_url'] = game_image.image_url if game_image else None
            games_with_images.append(game_data)
        
        return Response({'wishlist': games_with_images}, status=status.HTTP_200_OK)

class GameList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        
        games_with_images = []
        for game, game_data in zip(games, serializer.data):
            game_image = GameImage.objects.filter(game=game).first()
            game_data['image_url'] = game_image.image_url if game_image else None
            games_with_images.append(game_data)
        
        return Response({'games': games_with_images})
