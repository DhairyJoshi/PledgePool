from django.shortcuts import render

# Create your views here.
def home(request):
    is_logged_in = 'user_id' in request.session
    username = request.session.get('username', '')
    return render(request, 'index.html', {'is_logged_in': is_logged_in, 'username': username})

def services(request):
    return render(request, 'services.html')