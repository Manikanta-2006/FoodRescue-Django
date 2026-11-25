from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def donor_required(view_func):
    """
    Decorator to ensure the authenticated user has a 'Donor' role or is a superuser.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access this page.")
            return redirect('accounts:login')
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        if hasattr(request.user, 'profile') and request.user.profile.role == 'Donor':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access restricted: This section is only accessible to Food Donors.")
        return redirect('accounts:dashboard_redirect')
    return _wrapped_view


def ngo_required(view_func):
    """
    Decorator to ensure the authenticated user has an 'NGO' role or is a superuser.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access this page.")
            return redirect('accounts:login')
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        if hasattr(request.user, 'profile') and request.user.profile.role == 'NGO':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access restricted: This section is only accessible to NGOs and Charitable Receivers.")
        return redirect('accounts:dashboard_redirect')
    return _wrapped_view


def volunteer_required(view_func):
    """
    Decorator to ensure the authenticated user has a 'Volunteer' role or is a superuser.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access this page.")
            return redirect('accounts:login')
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        if hasattr(request.user, 'profile') and request.user.profile.role == 'Volunteer':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access restricted: This section is only accessible to Food Rescue Volunteers.")
        return redirect('accounts:dashboard_redirect')
    return _wrapped_view
