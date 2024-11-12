"""
Definition of models.
"""

from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    registration_date = models.DateField()

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    developer = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    description = models.TextField()
    average_rating = models.FloatField()

class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=100)

class GamePlatform(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)

class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

class GameGenre(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class GameImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    image_url = models.URLField()
    caption = models.CharField(max_length=255)

class Developer(models.Model):
    developer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    founded_date = models.DateField()
    country = models.CharField(max_length=100)

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.FloatField()
    review_text = models.TextField()
    review_date = models.DateField()
