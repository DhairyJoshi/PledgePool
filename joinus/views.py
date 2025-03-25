from django.shortcuts import render

# Create your views here.

def whycreator(request):
    return render(request, 'whycreator.html')

def whybacker(request):
    return render(request, 'whybacker.html')