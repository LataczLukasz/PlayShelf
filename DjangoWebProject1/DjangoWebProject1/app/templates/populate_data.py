# populate_data.py

import django
import os

# Ustawienia Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from app.models import User, Game, Platform, Genre, Developer, Review

# Przykładowi użytkownicy
user1 = User.objects.create(username="janek123", password="password123", email="janek@example.com", registration_date="2023-01-01")
user2 = User.objects.create(username="ania456", password="password456", email="ania@example.com", registration_date="2023-02-01")

# Przykładowe gry
game1 = Game.objects.create(title="Gra XYZ", release_date="2021-06-15", developer="Dev Studios", publisher="XYZ Corp", description="Przygoda w fantastycznym świecie.", average_rating=4.5)
game2 = Game.objects.create(title="Gra ABC", release_date="2022-09-10", developer="ABC Studios", publisher="ABC Inc", description="Akcja pełna emocji.", average_rating=4.0)

# Przykładowe platformy
platform1 = Platform.objects.create(name="PC", manufacturer="Microsoft")
platform2 = Platform.objects.create(name="PlayStation", manufacturer="Sony")

# Przykładowe gatunki
genre1 = Genre.objects.create(name="RPG")
genre2 = Genre.objects.create(name="Action")

# Przykładowi deweloperzy
developer1 = Developer.objects.create(name="Dev Studios", founded_date="2010-05-20", country="Polska")
developer2 = Developer.objects.create(name="ABC Studios", founded_date="2005-11-30", country="USA")

# Przykładowe recenzje
review1 = Review.objects.create(user=user1, game=game1, rating=5.0, review_text="Świetna gra!", review_date="2023-04-20")
review2 = Review.objects.create(user=user2, game=game2, rating=4.5, review_text="Bardzo dobra gra, ale z drobnymi błędami.", review_date="2023-04-21")
