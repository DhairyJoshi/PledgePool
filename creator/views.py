from django.shortcuts import render, redirect
from accounts.models import pledgepool_user
from django.contrib import messages

def dashboard(request):
    if request.session.get('role') != 'creator':
        messages.error(request, "You are not authorized to view this page.")
        return redirect('login')
    return render(request, 'creator_dashboard.html')