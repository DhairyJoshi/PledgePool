from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import pledgepool_user
from django.db import IntegrityError

# Create your views here.

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email'].strip().lower()
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST['phone']
        role = request.POST['role']
        birthdate = request.POST['birthdate']
        pfp = request.FILES.get('pfp')
        description = request.POST['description']

        name = f"{fname} {lname}"

        if password != confirm_password:
            messages.error(request, "The passwords you entered do not match. Please try again.")
            return redirect('register')

        if pledgepool_user.objects.filter(username=username).exists():
            messages.error(request, f"The username {username} is already taken. Please try a different one.")
            return redirect('register')

        if pledgepool_user.objects.filter(email=email).exists():
            messages.error(request, f"The email {email} is already registered. Please use a different one.")
            return redirect('register')

        try:
            user = pledgepool_user(
                name=name,
                username=username,
                email=email,
                password=password,
                role=role,
                phone=phone,
                birthdate=birthdate,
                pfp=pfp,
                description=description
            )
            print("FILES:", request.FILES)
            print("pfp:", request.FILES.get('pfp'))
            user.save()
            messages.success(request, f"User {username} has been successfully created.")
            return redirect('register')
        except IntegrityError:
            messages.error(request, "Unknown Error Occured")
            return redirect('register')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = pledgepool_user.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['role'] = user.role

            if user.role == 'creator':
                messages.success(request, f"Welcome back, {username}!")
                return redirect('../creator/dashboard')
            elif user.role == 'backer':
                messages.success(request, f"Welcome back, {username}!")
                return redirect('../backer/dashboard')
            else:
                messages.error(request, "Invalid role detected.")
                return redirect('login')
            
        except pledgepool_user.DoesNotExist:
            messages.error(request, "The username or password you entered is incorrect. Please try again.")
            return redirect('login')

    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return render(request, 'logout.html')