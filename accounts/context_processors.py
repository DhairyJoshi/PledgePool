from .models import pledgepool_user  # Adjust this import based on your app structure

def user_context(request):
    username = request.session.get('username', '')
    user_obj = None

    if username:
        try:
            user_obj = pledgepool_user.objects.get(username=username)
        except pledgepool_user.DoesNotExist:
            user_obj = None 

    return {
        'user_name': username,
        'user_role': request.session.get('role', ''),
        'is_logged_in': request.session.get('user_id') is not None,
        'user_obj': user_obj
    }
