def user_context(request):
    return {
        'user_name': request.session.get('name', ''),
        'user_role': request.session.get('role', ''),
        'is_logged_in': request.session.get('user_id') is not None,
    }