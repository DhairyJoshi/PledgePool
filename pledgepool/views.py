from django.shortcuts import render, redirect
from accounts.models import pledgepool_user
from django.contrib import messages

# Create your views here.
def home(request):
    role = request.session.get('role')

    if role == 'creator':
        return redirect('/creator/dashboard')
    elif role == 'backer':
        return redirect('/backer/dashboard')
    
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')