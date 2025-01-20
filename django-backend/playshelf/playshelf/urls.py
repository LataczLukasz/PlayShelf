from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from playshelfapp import forms, views
from playshelfapp.views import CustomTokenObtainPairView, LogoutView, UserRegistrationView, GameList, GameRatingsView, GameRatingsEditView

urlpatterns = [
    path('', views.home, name='home'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('games/', GameList.as_view(), name='games_list'),
    path('rating/<game_id>', GameRatingsView.as_view(), name='games_rating_view'),
    path('games/review/add/', GameRatingsEditView.as_view(), name='games_rating_add_view'),
    path('admin/', admin.site.urls),
    path('', include('playshelfapp.urls')),
]