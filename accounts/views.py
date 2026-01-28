from django.shortcuts import render, redirect
from django.contrib import messages
from .models import pledgepool_user
from django.db import IntegrityError
from django.utils import timezone
from projects.models import Pledge, Campaign
from django.db.models import Sum, Count

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

def profile(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    try:
        user = pledgepool_user.objects.get(id=request.session.get('user_id'))
    except pledgepool_user.DoesNotExist:
        return redirect('login')
    
    return render(request, 'profile.html', {
        'user': user
    })

def edit_profile(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    try:
        user = pledgepool_user.objects.get(id=request.session.get('user_id'))
    except pledgepool_user.DoesNotExist:
        return redirect('login')
    
    if request.method == 'POST':
        # Update user profile
        user.name = request.POST.get('name', user.name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.description = request.POST.get('description', user.description)
        
        # Handle profile picture upload
        if 'pfp' in request.FILES:
            user.pfp = request.FILES['pfp']
        
        try:
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    return render(request, 'edit_profile.html', {
        'user': user
    })

def settings(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    try:
        user = pledgepool_user.objects.get(id=request.session.get('user_id'))
    except pledgepool_user.DoesNotExist:
        return redirect('login')
    
    if request.method == 'POST':
        # Handle password change
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if current_password and new_password and confirm_password:
            if user.password == current_password:  # In production, use proper password hashing
                if new_password == confirm_password:
                    user.password = new_password
                    user.save()
                    messages.success(request, 'Password changed successfully!')
                else:
                    messages.error(request, 'New passwords do not match!')
            else:
                messages.error(request, 'Current password is incorrect!')
        
        # Handle account deletion
        if 'delete_account' in request.POST:
            # Add confirmation logic here
            user.delete()
            request.session.flush()
            messages.success(request, 'Account deleted successfully!')
            return redirect('login')
    
    return render(request, 'settings.html', {
        'user': user
    })

def my_pledges(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    try:
        user = pledgepool_user.objects.get(id=request.session.get('user_id'))
    except pledgepool_user.DoesNotExist:
        return redirect('login')
    
    # Get all pledges made by the user
    pledges = Pledge.objects.filter(backer=user).select_related('project', 'creator')
    
    # Get search query
    search_query = request.GET.get('search', '')
    if search_query:
        pledges = pledges.filter(project__title__icontains=search_query)
    
    # Get sort parameter
    sort_by = request.GET.get('sort', 'date_pledged')
    if sort_by == 'amount':
        pledges = pledges.order_by('-amount')
    elif sort_by == 'project_title':
        pledges = pledges.order_by('project__title')
    elif sort_by == 'date_pledged':
        pledges = pledges.order_by('-date_pledged')
    else:
        pledges = pledges.order_by('-date_pledged')
    
    # Calculate total pledged amount
    total_pledged = pledges.aggregate(total=Sum('amount'))['total'] or 0
    
    # Get unique campaigns count
    campaigns_count = pledges.values('project').distinct().count()
    
    # Group pledges by campaign for better display
    campaign_pledges = {}
    for pledge in pledges:
        campaign = pledge.project
        if campaign.id not in campaign_pledges:
            campaign_pledges[campaign.id] = {
                'campaign': campaign,
                'pledges': [],
                'total_pledged': 0,
                'pledge_count': 0
            }
        campaign_pledges[campaign.id]['pledges'].append(pledge)
        campaign_pledges[campaign.id]['total_pledged'] += pledge.amount
        campaign_pledges[campaign.id]['pledge_count'] += 1
    
    # Convert to list and sort
    campaign_pledges_list = list(campaign_pledges.values())
    if sort_by == 'amount':
        campaign_pledges_list.sort(key=lambda x: x['total_pledged'], reverse=True)
    elif sort_by == 'project_title':
        campaign_pledges_list.sort(key=lambda x: x['campaign'].title)
    elif sort_by == 'date_pledged':
        campaign_pledges_list.sort(key=lambda x: max(p.date_pledged for p in x['pledges']), reverse=True)
    
    return render(request, 'my_pledges.html', {
        'user': user,
        'campaign_pledges': campaign_pledges_list,
        'total_pledged': total_pledged,
        'campaigns_count': campaigns_count,
        'search_query': search_query,
        'sort_by': sort_by
    })