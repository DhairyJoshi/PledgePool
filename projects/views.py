from django.shortcuts import render, redirect

# Create your views here.

def viewprojects(request):
    return render(request, 'viewprojects.html')


def createproject(request):
    return render(request, 'create_project.html')