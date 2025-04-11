from django.shortcuts import render, redirect
from accounts.models import pledgepool_user
from django.contrib import messages

def dashboard(request):
    if request.session.get('role') != 'creator':
        return redirect('access-denied')
    return render(request, 'creator_dashboard.html')