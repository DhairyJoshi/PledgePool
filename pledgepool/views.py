from django.shortcuts import render
from accounts.models import pledgepool_user

# Create your views here.
def home(request):
    is_logged_in = 'user_id' in request.session
    username = request.session.get('username', '')
    user_obj = None

    if username:
        try:
            user_obj = pledgepool_user.objects.get(username=username)
        except pledgepool_user.DoesNotExist:
            pass

    return render(request, 'index.html', {
        'is_logged_in': is_logged_in,
        'username': username,
        'user_obj': user_obj
    })

def services(request):
    return render(request, 'services.html')