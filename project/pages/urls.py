from django.urls import path

from .views import home, profile, about_us, clients

urlpatterns = [
    path('', home, name='home'),
    path('profile', profile, name='profile'),
    path('about_us', about_us, name='about_us'),
    path('clients', clients, name='clients'),
]
