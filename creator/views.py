from django.shortcuts import render, redirect
from accounts.models import pledgepool_user
from projects.models import Campaign
from django.utils import timezone
from datetime import timedelta

def dashboard(request):
    if request.session.get('role') != 'creator':
        return redirect('access-denied')
    return render(request, 'creator_dashboard.html')


from datetime import timedelta

def myprojects(request):
    if request.session.get('role') != 'creator':
        return redirect('access-denied')

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('../accounts/login')

    try:
        user = pledgepool_user.objects.get(id=user_id)
    except pledgepool_user.DoesNotExist:
        return redirect('../accounts/login')

    # Get all projects for this creator
    projects = Campaign.objects.filter(creator=user)

    today = timezone.now().date()

    # Add days_left to each project
    for project in projects:
        if project.end_date:
            delta = project.end_date - today
            project.days_left = max(delta.days, 0)  # Avoid negative days
        else:
            project.days_left = 0

    return render(request, 'creator_projects.html', {
        'projects': projects
    })