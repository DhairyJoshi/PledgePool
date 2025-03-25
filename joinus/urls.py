from django.urls import path
from . import views

urlpatterns = [
    path('whycreator', views.whycreator, name='whycreator'),
    path('whybacker', views.whybacker, name='whybacker'),
]