from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import pledgepool_user
from projects.models import Campaign, CampaignGalleryImage
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

def dashboard(request):
    if request.session.get('role') != 'creator':
        return redirect('access-denied')
    return render(request, 'creator_dashboard.html')

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

    # Calculate statistics
    total_raised = sum(project.achieved_funding for project in projects)
    active_projects_count = sum(1 for project in projects if project.end_date > today)

    # Add days_left to each project
    for project in projects:
        if project.end_date:
            delta = project.end_date - today
            project.days_left = max(delta.days, 0)  # Avoid negative days
        else:
            project.days_left = 0

        # Calculate remaining amount
        project.remaining_amount = max(project.funding_goal - project.achieved_funding, 0)

        if project.funding_goal > 0:
            progress = (project.achieved_funding / project.funding_goal) * 100
            project.campaign_progress = min(round(progress, 2), 100)  # Cap at 100%
        else:
            project.campaign_progress = 0

    return render(request, 'creator_projects.html', {
        'projects': projects,
        'total_raised': total_raised,
        'active_projects_count': active_projects_count,
        'today': today,
    })

def edit_project(request, project_id):
    """Edit project view - supports read, update, and delete"""
    if request.session.get('role') != 'creator':
        return redirect('access-denied')

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('../accounts/login')

    try:
        user = pledgepool_user.objects.get(id=user_id)
    except pledgepool_user.DoesNotExist:
        return redirect('../accounts/login')

    # Get the project and ensure it belongs to the current user
    project = get_object_or_404(Campaign, id=project_id, creator=user)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'delete':
            # Handle delete
            project_title = project.title
            project.delete()
            messages.success(request, f"Campaign '{project_title}' has been deleted successfully!")
            return redirect('myprojects')
        
        elif action == 'update':
            # Handle update
            try:
                # Get form values
                project.title = request.POST.get('title')
                project.category = request.POST.get('category')
                project.funding_goal = request.POST.get('funding_goal')
                project.description = request.POST.get('description')
                project.start_date = request.POST.get('start_date')
                project.end_date = request.POST.get('end_date')
                project.detailed_description = request.POST.get('detailed_description')
                project.problem_statement = request.POST.get('problem_statement')
                project.funds_use = request.POST.get('funds_use')
                project.video_url = request.POST.get('video_url')
                project.reward_title = request.POST.get('reward_title')
                project.reward_description = request.POST.get('reward_description')
                project.delivery = request.POST.get('delivery_date')
                project.agreements = request.POST.get('agreements')

                # Handle campaign cover update
                campaign_cover = request.FILES.get('campaign_cover')
                if campaign_cover:
                    project.campaign_cover = campaign_cover

                # Handle gallery images update
                campaign_gallery_files = request.FILES.getlist('campaign_gallery')
                if campaign_gallery_files:
                    # Delete existing gallery images
                    project.gallery_images.all().delete()
                    # Add new gallery images
                    for image_file in campaign_gallery_files:
                        CampaignGalleryImage.objects.create(
                            campaign=project,
                            image=image_file
                        )

                project.save()
                messages.success(request, f"Campaign '{project.title}' updated successfully!")
                return redirect('edit_project', project_id=project.id)

            except Exception as e:
                messages.error(request, f"An error occurred while updating the campaign: {str(e)}")
                return redirect('edit_project', project_id=project.id)

    # For GET request, just display the form
    return render(request, 'edit_project.html', {
        'project': project
    })

@require_POST
@csrf_exempt
def delete_project_ajax(request, project_id):
    """AJAX endpoint for deleting projects"""
    if request.session.get('role') != 'creator':
        return JsonResponse({'success': False, 'message': 'Access denied'})

    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'User not authenticated'})

    try:
        user = pledgepool_user.objects.get(id=user_id)
        project = get_object_or_404(Campaign, id=project_id, creator=user)
        
        project_title = project.title
        project.delete()
        
        return JsonResponse({
            'success': True, 
            'message': f"Campaign '{project_title}' deleted successfully!"
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': f"Error deleting campaign: {str(e)}"
        })