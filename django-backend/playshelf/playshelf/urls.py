from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from playshelfapp import forms, views
from playshelfapp.views import CustomTokenObtainPairView, LogoutView, UserRegistrationView, GameList

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('games/', GameList.as_view(), name='games_list'),
    # path('login/',
    #      LoginView.as_view
    #      (
    #          template_name='playshelfapp/login.html',
    #          authentication_form=forms.BootstrapAuthenticationForm,
    #          extra_context=
    #          {
    #              'title': 'Log in',
    #              'year' : datetime.now().year,
    #          }
    #      ),
    #      name='login'),
    # path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('', include('playshelfapp.urls')),
]