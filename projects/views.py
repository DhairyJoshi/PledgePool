from django.shortcuts import render, redirect
from .models import Campaign, pledgepool_user
from django.contrib import messages
from decimal import Decimal

def viewprojects(request):
    return render(request, 'viewprojects.html')

def createproject(request):
    if request.session.get('role') != 'creator':
        return redirect('access-denied')
    
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('../accounts/login')

        try:
            user = pledgepool_user.objects.get(id=user_id)
        except pledgepool_user.DoesNotExist:
            return redirect('../accounts/login')

        title = request.POST.get('title')
        category = request.POST.get('category')
        funding_goal = request.POST.get('funding_goal')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        detailed_description = request.POST.get('detailed_description')
        problem_statement = request.POST.get('problem_statement')
        funds_use = request.POST.get('funds_use')
        video_url = request.POST.get('video_url')

        reward_title = request.POST.get('reward_title')
        reward_description = request.POST.get('reward_description')
        delivery = request.POST.get('delivery_date')
        agreements = request.POST.get('agreements')  # Fixed key here

        # file uploads
        campaign_cover = request.FILES.get('campaign_cover')
        campaign_gallery = request.FILES.get('campaign_gallery')

        try:
            Campaign.objects.create(
                creator=user,
                title=title,
                category=category,
                funding_goal=funding_goal,
                achieved_funding = 0,
                description=description,
                start_date=start_date,
                end_date=end_date,
                detailed_description=detailed_description,
                problem_statement=problem_statement,
                funds_use=funds_use,
                campaign_cover=campaign_cover,
                video_url=video_url,
                campaign_gallery=campaign_gallery,
                reward_title=reward_title,
                reward_description=reward_description,
                delivery=delivery,
                agreements=agreements,
            )
            messages.success(request, f"Campaign '{title}' created successfully!")
            return redirect('../projects/create')
        except Exception as e:
            messages.error(request, f"An error occurred while creating the campaign: {str(e)}")
            return redirect('../projects/create')

    return render(request, 'create_project.html')