
# scripts.py
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from myapp.models import User, Game

# Tworzenie nowego u¿ytkownika
user = User.objects.create(username="testuser", password="password", email="test@example.com", registration_date="2023-01-01")

# Pobieranie wszystkich gier
games = Game.objects.all()
for game in games:
    print(game.title, game.average_rating)
