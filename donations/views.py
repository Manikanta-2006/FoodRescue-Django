from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.contrib.auth.models import User

from accounts.decorators import donor_required
from accounts.models import UserProfile
from .models import Donation
from .forms import DonationForm


def home_view(request):
    """
    Public landing page featuring mission hero, database-driven live statistics,
    available food donations, how-it-works, and call-to-actions.
    """
    # Live database statistics
    total_donations_count = Donation.objects.count()
    active_donations_count = Donation.objects.filter(status='AVAILABLE', expiry_at__gt=timezone.now()).count()
    completed_deliveries_count = Donation.objects.filter(status='DELIVERED').count()
    
    # Calculate approximate meals rescued (sum of all completed or available quantities)
    total_quantity_rescued = Donation.objects.filter(
        status__in=['DELIVERED', 'COLLECTED', 'ACCEPTED', 'AVAILABLE']
    ).aggregate(total=Sum('quantity'))['total'] or 0

    verified_ngos_count = UserProfile.objects.filter(role='NGO', is_verified=True).count()
    volunteers_count = UserProfile.objects.filter(role='Volunteer').count()

    # Featured available donations
    featured_donations = Donation.objects.filter(
        status='AVAILABLE',
        expiry_at__gt=timezone.now()
    ).select_related('donor', 'donor__profile').order_by('expiry_at')[:6]

    context = {
        'total_donations': total_donations_count,
        'active_donations': active_donations_count,
        'completed_deliveries': completed_deliveries_count,
        'meals_rescued': int(total_quantity_rescued),
        'verified_ngos': verified_ngos_count,
        'volunteers_count': volunteers_count,
        'featured_donations': featured_donations,
        'title': 'FoodRescue - Rescue Food, Share Hope',
    }
    return render(request, 'donations/home.html', context)


def about_view(request):
    """
    About Us page explaining the food waste crisis, sustainable goals, and platform mission.
    """
    return render(request, 'donations/about.html', {'title': 'About FoodRescue Initiative'})


def how_it_works_view(request):
    """
    Explains the 3-tier food redistribution workflow for Donors, NGOs, and Volunteers.
    """
    return render(request, 'donations/how_it_works.html', {'title': 'How FoodRescue Works'})


def contact_view(request):
    """
    Contact and feedback page with POST processing and feedback notification.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            messages.success(
                request,
                f"Thank you, {name}! Your message regarding '{subject or 'General Inquiry'}' has been received. "
                "Our team will contact you shortly."
            )
            return redirect('donations:contact')
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, 'donations/contact.html', {'title': 'Contact FoodRescue Team'})


def donation_list_view(request):
    """
    Browse all food donations with full database-driven search, category filtering,
    location filtering, and status filtering.
    """
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    city = request.GET.get('city', '').strip()
    status = request.GET.get('status', 'AVAILABLE').strip()

    # Base queryset
    donations = Donation.objects.select_related('donor', 'donor__profile').all()

    # Apply status filter
    if status and status != 'ALL':
        if status == 'AVAILABLE':
            donations = donations.filter(status='AVAILABLE', expiry_at__gt=timezone.now())
        else:
            donations = donations.filter(status=status)

    # Search filter by food name, description, address
    if query:
        donations = donations.filter(
            Q(food_name__icontains=query) |
            Q(description__icontains=query) |
            Q(pickup_address__icontains=query) |
            Q(city__icontains=query)
        )

    # Category filter
    if category:
        donations = donations.filter(category=category)

    # City / Location filter
    if city:
        donations = donations.filter(city__icontains=city)

    # Order by nearest expiry first for active, else newest
    donations = donations.order_by('expiry_at')

    # Distinct categories and cities for dropdown filters
    categories = Donation.CATEGORY_CHOICES
    cities = Donation.objects.values_list('city', flat=True).distinct().order_by('city')

    context = {
        'donations': donations,
        'categories': categories,
        'cities': cities,
        'current_q': query,
        'current_category': category,
        'current_city': city,
        'current_status': status,
        'total_count': donations.count(),
        'title': 'Browse Food Donations',
    }
    return render(request, 'donations/donation_list.html', context)


def donation_detail_slug_view(request, slug):
    """
    Academic requirement: slug path converter.
    Displays complete donation details identified by its unique slug.
    """
    donation = get_object_or_404(Donation.objects.select_related('donor', 'donor__profile'), slug=slug)
    
    # Check if current user is an NGO and has already requested this donation
    user_request = None
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.is_ngo:
        user_request = donation.requests.filter(receiver=request.user).first()

    context = {
        'donation': donation,
        'user_request': user_request,
        'title': f"{donation.food_name} - Donation Details",
    }
    return render(request, 'donations/donation_detail.html', context)


def donation_detail_id_view(request, pk):
    """
    Academic requirement: int path converter.
    Redirects or displays donation identified by its primary key ID.
    """
    donation = get_object_or_404(Donation, pk=pk)
    return redirect('donations:donation_detail_slug', slug=donation.slug)


def donation_category_view(request, category_code):
    """
    Academic requirement: re_path regex pattern.
    Handles regex matched category code and filters donations accordingly.
    """
    valid_codes = [c[0] for c in Donation.CATEGORY_CHOICES]
    cat_upper = category_code.upper()

    if cat_upper not in valid_codes:
        raise Http404(f"Food category '{category_code}' does not exist.")

    donations = Donation.objects.filter(
        category=cat_upper,
        status='AVAILABLE',
        expiry_at__gt=timezone.now()
    ).select_related('donor', 'donor__profile').order_by('expiry_at')

    cat_name = dict(Donation.CATEGORY_CHOICES).get(cat_upper, category_code)

    context = {
        'donations': donations,
        'category_name': cat_name,
        'category_code': cat_upper,
        'total_count': donations.count(),
        'title': f"Donations: {cat_name}",
    }
    return render(request, 'donations/donation_by_category.html', context)


def api_donations_json_view(request):
    """
    Academic requirement: JsonResponse endpoint.
    Returns JSON list of available food donations for API clients or live search.
    """
    q = request.GET.get('q', '').strip()
    donations_qs = Donation.objects.filter(status='AVAILABLE', expiry_at__gt=timezone.now())

    if q:
        donations_qs = donations_qs.filter(
            Q(food_name__icontains=q) |
            Q(category__icontains=q) |
            Q(city__icontains=q)
        )

    data = []
    for d in donations_qs[:25]:
        data.append({
            'id': d.id,
            'slug': d.slug,
            'food_name': d.food_name,
            'category': d.get_category_display(),
            'quantity': float(d.quantity),
            'unit': d.get_unit_display(),
            'city': d.city,
            'pickup_address': d.pickup_address,
            'expiry_at': d.expiry_at.strftime('%Y-%m-%d %H:%M'),
            'image_url': d.get_image_url,
            'detail_url': d.get_absolute_url(),
        })

    return JsonResponse({
        'status': 'success',
        'count': len(data),
        'donations': data
    }, safe=False)


def api_stats_json_view(request):
    """
    Academic requirement: JsonResponse endpoint.
    Returns live platform statistics as JSON.
    """
    stats = {
        'total_donations': Donation.objects.count(),
        'available_donations': Donation.objects.filter(status='AVAILABLE').count(),
        'delivered_donations': Donation.objects.filter(status='DELIVERED').count(),
        'registered_users': User.objects.count(),
        'verified_ngos': UserProfile.objects.filter(role='NGO', is_verified=True).count(),
        'volunteers': UserProfile.objects.filter(role='Volunteer').count(),
        'timestamp': timezone.now().isoformat(),
    }
    return JsonResponse(stats)


# ==============================================================================
# DONOR VIEWS (Protected with @donor_required)
# ==============================================================================

@donor_required
def donor_dashboard_view(request):
    """
    Donor Dashboard displaying key metrics, recent donations, and incoming request alerts.
    """
    user_donations = Donation.objects.filter(donor=request.user)
    
    total_posted = user_donations.count()
    available_count = user_donations.filter(status='AVAILABLE').count()
    completed_count = user_donations.filter(status='DELIVERED').count()
    
    # Incoming requests across all donations posted by this donor
    incoming_requests = request.user.donations.filter(
        requests__status='PENDING'
    ).values_list('requests__id', flat=True)
    pending_requests_count = len(incoming_requests)

    recent_donations = user_donations.order_by('-created_at')[:5]

    context = {
        'total_posted': total_posted,
        'available_count': available_count,
        'completed_count': completed_count,
        'pending_requests_count': pending_requests_count,
        'recent_donations': recent_donations,
        'title': 'Donor Portal - Dashboard',
    }
    return render(request, 'donations/donor_dashboard.html', context)


@donor_required
def donor_add_donation_view(request):
    """
    Create a new food donation with image upload and validation.
    """
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            messages.success(
                request,
                f"Your food donation '{donation.food_name}' has been posted successfully! "
                "Nearby NGOs can now view and request it."
            )
            return redirect('donations:donor_my_donations')
        else:
            messages.error(request, "Please review the form errors below.")
    else:
        # Prepopulate pickup address and city from donor profile if available
        initial_data = {}
        if hasattr(request.user, 'profile'):
            initial_data['pickup_address'] = request.user.profile.address
            initial_data['city'] = request.user.profile.city
        form = DonationForm(initial=initial_data)

    context = {
        'form': form,
        'title': 'Post Surplus Food Donation',
    }
    return render(request, 'donations/donor_add_donation.html', context)


@donor_required
def donor_my_donations_view(request):
    """
    List all donations posted by the logged-in donor with status filters and management actions.
    """
    status_filter = request.GET.get('status', 'ALL')
    donations = Donation.objects.filter(donor=request.user).prefetch_related('requests')

    if status_filter != 'ALL':
        donations = donations.filter(status=status_filter)

    donations = donations.order_by('-created_at')

    context = {
        'donations': donations,
        'current_status': status_filter,
        'title': 'My Food Donations',
    }
    return render(request, 'donations/donor_my_donations.html', context)


@donor_required
def donor_edit_donation_view(request, pk):
    """
    Edit an existing donation created by the logged-in donor.
    """
    donation = get_object_or_404(Donation, pk=pk, donor=request.user)

    if donation.status in ['COLLECTED', 'DELIVERED']:
        messages.error(request, "This donation is already in transit or delivered and cannot be edited.")
        return redirect('donations:donor_my_donations')

    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES, instance=donation)
        if form.is_valid():
            form.save()
            messages.success(request, f"Donation '{donation.food_name}' updated successfully.")
            return redirect('donations:donor_my_donations')
        else:
            messages.error(request, "Please fix the errors indicated below.")
    else:
        form = DonationForm(instance=donation)

    context = {
        'form': form,
        'donation': donation,
        'title': f"Edit Donation: {donation.food_name}",
    }
    return render(request, 'donations/donor_edit_donation.html', context)


@donor_required
def donor_delete_donation_view(request, pk):
    """
    Delete a donation posted by the logged-in donor.
    """
    donation = get_object_or_404(Donation, pk=pk, donor=request.user)

    if request.method == 'POST':
        food_name = donation.food_name
        donation.delete()
        messages.success(request, f"Donation '{food_name}' has been successfully deleted.")
        return redirect('donations:donor_my_donations')

    context = {
        'donation': donation,
        'title': f"Delete Donation: {donation.food_name}",
    }
    return render(request, 'donations/donor_delete_confirm.html', context)


# ==============================================================================
# ADMIN PLATFORM OVERVIEW DASHBOARD (Academic & Viva Showcase)
# ==============================================================================

@login_required
def admin_dashboard_view(request):
    """
    Platform overview dashboard for administrators and faculty viva demonstration.
    Presents complete ecosystem metrics, latest users, donations, requests, and deliveries.
    """
    if not (request.user.is_superuser or request.user.is_staff):
        messages.warning(request, "Administrative overview is reserved for authorized platform staff.")
        return redirect('accounts:dashboard_redirect')

    all_donations = Donation.objects.select_related('donor', 'donor__profile').order_by('-created_at')[:10]
    all_users = User.objects.select_related('profile').order_by('-date_joined')[:10]
    total_users = User.objects.count()
    total_donations = Donation.objects.count()
    total_deliveries = Donation.objects.filter(status='DELIVERED').count()

    context = {
        'all_donations': all_donations,
        'all_users': all_users,
        'total_users': total_users,
        'total_donations': total_donations,
        'total_deliveries': total_deliveries,
        'title': 'Platform Administration & Overview',
    }
    return render(request, 'donations/admin_dashboard.html', context)
