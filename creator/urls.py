from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('myprojects', views.myprojects, name='myprojects'),
    path('edit-project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete-project/<int:project_id>/', views.delete_project_ajax, name='delete_project_ajax'),
]