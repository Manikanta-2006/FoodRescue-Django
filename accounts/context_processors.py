def user_role_context(request):
    """
    Context processor to provide user role flags and profile safely to all templates.
    """
    context = {
        'user_profile': None,
        'is_donor': False,
        'is_ngo': False,
        'is_volunteer': False,
        'is_verified_ngo': False,
    }
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            context['user_profile'] = profile
            context['is_donor'] = (profile.role == 'Donor')
            context['is_ngo'] = (profile.role == 'NGO')
            context['is_volunteer'] = (profile.role == 'Volunteer')
            context['is_verified_ngo'] = (profile.role == 'NGO' and profile.is_verified)
        except Exception:
            pass
    return context
