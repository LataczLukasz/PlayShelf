from django.utils import timezone
from rest_framework import serializers
from .models import (
    User, Game, Platform, GamePlatform, Genre, GameGenre, Wishlist, 
    GameImage, Developer, Review
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'

class GamePlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePlatform
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class GameGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameGenre
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

class GameImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameImage
        fields = '__all__'

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = authenticate(email=credentials['email'], password=credentials['password'])

        if not user:
            raise AuthenticationFailed('Nieprawidłowe dane logowania.')

        data = super().validate(attrs)
        refresh = self.get_token(user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = user.username
        data['email'] = user.email
        data['user_id'] = user.user_id
        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'registration_date']
        extra_kwargs = {
            'password': {'write_only': True},  # Ukryj hasło w odpowiedzi
            'registration_date': {'read_only': True},  # Automatyczna data rejestracji
        }

    def create(self, validated_data):
        # Hashowanie hasła przed zapisaniem
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['registration_date'] = validated_data.get('registration_date') or timezone.now().date()
        return super().create(validated_data)

    def validate_email(self, value):
        # Opcjonalna walidacja dla e-maila
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("E-mail jest już zajęty.")
        return value