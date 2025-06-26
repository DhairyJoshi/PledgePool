from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path('settings', views.settings, name='settings'),
]