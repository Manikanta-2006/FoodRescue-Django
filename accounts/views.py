from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

from .forms import UserRegistrationForm, UserUpdateForm, UserProfileUpdateForm
from .models import UserProfile


def register_view(request):
    """
    Handle user registration with role specification (Donor, NGO, Volunteer).
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_redirect')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Profile is auto-created by signal with defaults; update with user's chosen role & details
            profile, created = UserProfile.objects.get_or_create(user=user)
            chosen_role = form.cleaned_data['role']
            profile.role = chosen_role
            profile.phone = form.cleaned_data['phone']
            profile.organization_name = form.cleaned_data['organization_name']
            profile.address = form.cleaned_data['address']
            profile.city = form.cleaned_data['city']
            # Verified automatically if donor or volunteer, NGO can be verified by admin
            if chosen_role in ['Donor', 'Volunteer']:
                profile.is_verified = True
            elif chosen_role == 'NGO':
                profile.is_verified = True  # Auto-verify demo NGOs or keep active
            profile.save()

            # Ensure user instance has the latest profile attached in memory
            user.refresh_from_db()

            login(request, user)
            messages.success(
                request,
                f"Welcome to FoodRescue, {user.first_name or user.username}! "
                f"Your {profile.get_role_display()} account has been created successfully."
            )
            return redirect('accounts:dashboard_redirect')
        else:
            messages.error(request, "Please correct the errors indicated below.")
    else:
        role_param = request.GET.get('role', 'Donor')
        form = UserRegistrationForm(initial={'role': role_param})

    context = {
        'form': form,
        'title': 'Create FoodRescue Account',
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    """
    Handle user login with role-based routing.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_redirect')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                role = getattr(user.profile, 'role', 'Member') if hasattr(user, 'profile') else 'Staff'
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}! Logged in as {role}.")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('accounts:dashboard_redirect')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'title': 'Sign In to FoodRescue',
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout_view(request):
    """
    Handle user logout and redirect to homepage.
    """
    logout(request)
    messages.info(request, "You have been safely signed out. Thank you for making a difference!")
    return redirect('donations:home')


@login_required
def dashboard_redirect_view(request):
    """
    Direct users to their specific dashboard based on their registered role.
    """
    if request.user.is_superuser:
        return redirect('donations:admin_dashboard')

    if hasattr(request.user, 'profile'):
        role = request.user.profile.role
        if role == 'Donor':
            return redirect('donations:donor_dashboard')
        elif role == 'NGO':
            return redirect('requests:ngo_dashboard')
        elif role == 'Volunteer':
            return redirect('requests:volunteer_dashboard')

    # Fallback to home if no role
    return redirect('donations:home')


@login_required
def profile_view(request):
    """
    View and edit current user's personal and profile information.
    """
    profile = request.user.profile

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile information has been updated successfully!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please fix the errors in your submission.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile,
        'title': 'My Profile & Account Settings',
    }
    return render(request, 'accounts/profile.html', context)


def role_info_view(request, role_name):
    """
    Academic requirement: str path converter.
    Displays information and benefits of a specific role (Donor, NGO, Volunteer).
    """
    valid_roles = {
        'donor': {
            'title': 'Food Donors',
            'headline': 'Turn Surplus Food into Smiles',
            'desc': 'Hotels, caterers, restaurants, and households can easily post surplus food in under 2 minutes.',
            'responsibilities': [
                'Post accurate quantity and expiry details.',
                'Ensure hygienic food packaging.',
                'Accept incoming requests from verified NGOs.',
                'Hand over packaged meals to assigned volunteers.'
            ],
            'badge': 'bg-success',
            'role_key': 'Donor'
        },
        'ngo': {
            'title': 'NGOs & Relief Shelters',
            'headline': 'Empowering Charities with Free Sustenance',
            'desc': 'Verified orphanages, soup kitchens, and charities can claim fresh, wholesome food for those in need.',
            'responsibilities': [
                'Browse real-time donations within your city.',
                'Submit timely requests with exact required quantities.',
                'Receive deliveries from volunteers at your door.',
                'Feed children, seniors, and disadvantaged communities.'
            ],
            'badge': 'bg-primary',
            'role_key': 'NGO'
        },
        'volunteer': {
            'title': 'Rescue Volunteers',
            'headline': 'The Vital Bridge of Compassion',
            'desc': 'Passionate heroes who pick up food from donors and swiftly transport it to local NGOs.',
            'responsibilities': [
                'Claim available pickup tasks in your vicinity.',
                'Inspect hygiene and temperature of packages.',
                'Update real-time delivery status in the portal.',
                'Deliver hope directly to feeding centers.'
            ],
            'badge': 'bg-warning text-dark',
            'role_key': 'Volunteer'
        }
    }

    key = role_name.lower()
    if key not in valid_roles:
        raise Http404(f"Role information for '{role_name}' is not recognized.")

    data = valid_roles[key]
    return render(request, 'accounts/role_info.html', {
        'role_data': data,
        'role_name': role_name,
        'title': f"Join as a {data['title']}"
    })
