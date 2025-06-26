from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import pledgepool_user
from projects.models import Campaign, Pledge
from django.utils import timezone
from django.contrib import messages
from decimal import Decimal
from projects.models import CampaignGalleryImage

def viewprojects(request):
    # Fixed categories for navbar
    CATEGORY_LIST = [
        'Art & Design', 'Film & Video', 'Games', 'Social Causes', 'Education',
        'Health & Wellness', 'Technology', 'Startups', 'Animals & Pets'
    ]

    # Count projects per category
    from django.db.models import Count
    category_counts = {}
    for cat in CATEGORY_LIST:
        if cat == 'Film & Video':
            # Combine Film & Video and Music counts
            film_video_count = Campaign.objects.filter(category__iexact='Film & Video').count()
            music_count = Campaign.objects.filter(category__iexact='Music').count()
            category_counts[cat] = film_video_count + music_count
        else:
            category_counts[cat] = Campaign.objects.filter(category__iexact=cat).count()
    total_count = Campaign.objects.all().count()

    # Filtering
    selected_category = request.GET.get('category')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort', 'trending')

    projects = Campaign.objects.all()
    if selected_category and selected_category != 'All':
        if selected_category == 'Film & Video':
            # Combine Film & Video and Music categories
            projects = projects.filter(category__iexact__in=['Film & Video', 'Music'])
        else:
            projects = projects.filter(category__iexact=selected_category)
    if search_query:
        projects = projects.filter(title__icontains=search_query)

    # Sorting
    if sort_by == 'newest':
        projects = projects.order_by('-start_date')
    elif sort_by == 'ending':
        projects = projects.order_by('end_date')
    elif sort_by == 'funded':
        projects = projects.order_by('-achieved_funding')
    else:  # trending (default)
        projects = projects.order_by('-total_pledges', '-achieved_funding')

    today = timezone.now().date()

    # Add days_left to each project
    for project in projects:
        if project.end_date:
            delta = project.end_date - today
            project.days_left = max(delta.days, 0)  # Avoid negative days
        else:
            project.days_left = 0

        # Calculate remaining amount
        project.remaining_amount = max(project.funding_goal - project.achieved_funding, 0)

        # Inside loop:
        if project.funding_goal > 0:
            progress = (Decimal(project.achieved_funding) / Decimal(project.funding_goal)) * Decimal(100)
            project.campaign_progress = f"{min(round(progress, 2), 100)}%"
        else:
            project.campaign_progress = "0%"

    return render(request, 'viewprojects.html', {
        'projects': projects,
        'categories': CATEGORY_LIST,
        'category_counts': category_counts,
        'total_count': total_count,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort_by': sort_by,
    })


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
        campaign_gallery_files = request.FILES.getlist('campaign_gallery')

        try:
            # Create and save the campaign instance
            campaign_instance = Campaign.objects.create(
                creator=user,
                title=title,
                category=category,
                funding_goal=funding_goal,
                achieved_funding=0,
                total_pledges=0,
                description=description,
                start_date=start_date,
                end_date=end_date,
                detailed_description=detailed_description,
                problem_statement=problem_statement,
                funds_use=funds_use,
                campaign_cover=campaign_cover,
                video_url=video_url,
                reward_title=reward_title,
                reward_description=reward_description,
                delivery=delivery,
                agreements=agreements,
            )
            campaign_instance.save()

            # If there's a gallery image, associate it with the campaign
            for image_file in campaign_gallery_files:
                CampaignGalleryImage.objects.create(
                    campaign=campaign_instance,
                    image=image_file
                )

            messages.success(request, f"Campaign '{title}' created successfully!")
            return redirect('../projects/create')

        except Exception as e:
            messages.error(request, f"An error occurred while creating the campaign: {str(e)}")
            return redirect('../projects/create')

    return render(request, 'create_project.html')


def projectdetails(request, project_id):
    project = get_object_or_404(Campaign, id=project_id)

    # Compute additional fields
    today = timezone.now().date()
    delta = project.end_date - today if project.end_date else 0
    project.days_left = max(delta.days, 0)
    project.remaining_amount = max(project.funding_goal - project.achieved_funding, 0)
    project.campaign_progress = (
        min(round((project.achieved_funding / project.funding_goal) * 100, 2), 100)
        if project.funding_goal > 0 else 0
    )

    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            backer_id = request.session.get('user_id')

            if not backer_id:
                messages.error(request, "You must be logged in to pledge.")
                return redirect('login')

            backer = pledgepool_user.objects.get(id=backer_id)

            if backer.role != 'backer':
                messages.error(request, "Only backers can pledge.")
                return redirect('projectdetails', project_id=project.id)

            if amount <= 0:
                messages.error(request, "Pledge amount must be greater than zero.")
                return redirect('projectdetails', project_id=project.id)

            Pledge.objects.create(
                project=project,
                backer=backer,
                creator=project.creator,
                amount=amount
            )

            project.achieved_funding += amount
            project.total_pledges += 1
            project.save()

            messages.success(request, f"You pledged ₹{amount} to {project.title}.")
            return redirect('projectdetails', project_id=project.id)

        except pledgepool_user.DoesNotExist:
            messages.error(request, "Backer not found.")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")

    return render(request, 'project_details.html', {
        'project': project
    })