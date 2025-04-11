from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('services', views.services, name='services'),
    path('access-denied', views.accessDenied, name='access-denied'),
]