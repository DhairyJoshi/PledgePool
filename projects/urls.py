from django.urls import path
from . import views

urlpatterns = [
    path('view', views.viewprojects, name='view'),
    path('create', views.createproject, name='create'),
    path('projectdetails/<int:project_id>/', views.projectdetails, name='projectdetails'),
]