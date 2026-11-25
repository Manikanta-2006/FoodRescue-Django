from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from accounts.decorators import ngo_required, donor_required, volunteer_required
from donations.models import Donation
from .models import FoodRequest, Delivery
from .forms import FoodRequestForm, DeliveryStatusUpdateForm


# ==============================================================================
# NGO / RECEIVER VIEWS
# ==============================================================================

@ngo_required
def ngo_dashboard_view(request):
    """
    NGO Dashboard: Summary of active requests, fulfilled food batches, and quick discovery.
    """
    user_requests = FoodRequest.objects.filter(receiver=request.user).select_related('donation', 'delivery')

    total_requests = user_requests.count()
    pending_count = user_requests.filter(status='PENDING').count()
    approved_count = user_requests.filter(status='APPROVED').count()
    completed_count = user_requests.filter(status='COMPLETED').count()

    recent_requests = user_requests.order_by('-requested_at')[:6]

    # Available food nearby
    nearby_donations = Donation.objects.filter(
        status='AVAILABLE',
        expiry_at__gt=timezone.now()
    ).select_related('donor', 'donor__profile').order_by('expiry_at')[:4]

    context = {
        'total_requests': total_requests,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'completed_count': completed_count,
        'recent_requests': recent_requests,
        'nearby_donations': nearby_donations,
        'title': 'NGO Receiving Portal - Dashboard',
    }
    return render(request, 'requests/ngo_dashboard.html', context)


@ngo_required
def request_food_view(request, donation_id):
    """
    Submit a formal food request for an available donation.
    """
    donation = get_object_or_404(Donation, pk=donation_id)

    # Check if donation is available
    if not donation.is_active:
        messages.error(request, "This food donation is no longer available or has passed its expiry.")
        return redirect('donations:donation_detail_slug', slug=donation.slug)

    # Prevent donor from requesting their own food
    if donation.donor == request.user:
        messages.error(request, "You cannot request a food donation you posted yourself.")
        return redirect('donations:donation_detail_slug', slug=donation.slug)

    # Check for existing pending/approved request from this NGO
    existing = FoodRequest.objects.filter(
        donation=donation,
        receiver=request.user,
        status__in=['PENDING', 'APPROVED']
    ).first()

    if existing:
        messages.warning(request, f"You already have a {existing.get_status_display().lower()} request for this donation.")
        return redirect('requests:ngo_my_requests')

    if request.method == 'POST':
        form = FoodRequestForm(request.POST, donation=donation)
        if form.is_valid():
            req = form.save(commit=False)
            req.donation = donation
            req.receiver = request.user
            req.status = 'PENDING'
            req.save()

            # Update donation status
            donation.status = 'REQUESTED'
            donation.save()

            messages.success(
                request,
                f"Your request for '{donation.food_name}' ({req.quantity_requested} {donation.unit}) has been submitted! "
                "The donor has been notified."
            )
            return redirect('requests:ngo_my_requests')
        else:
            messages.error(request, "Please fix the errors in your request.")
    else:
        # Initial quantity equals total available quantity
        form = FoodRequestForm(
            donation=donation,
            initial={'quantity_requested': donation.quantity}
        )

    context = {
        'donation': donation,
        'form': form,
        'title': f"Request Food: {donation.food_name}",
    }
    return render(request, 'requests/request_food.html', context)


@ngo_required
def ngo_my_requests_view(request):
    """
    Display all food requests made by the logged-in NGO with live status and delivery tracking.
    """
    status_filter = request.GET.get('status', 'ALL')
    user_requests = FoodRequest.objects.filter(receiver=request.user).select_related(
        'donation', 'donation__donor', 'delivery', 'delivery__volunteer'
    )

    if status_filter != 'ALL':
        user_requests = user_requests.filter(status=status_filter)

    user_requests = user_requests.order_by('-requested_at')

    context = {
        'requests': user_requests,
        'current_status': status_filter,
        'title': 'My Food Requests & Deliveries',
    }
    return render(request, 'requests/ngo_my_requests.html', context)


@ngo_required
def ngo_cancel_request_view(request, pk):
    """
    Cancel an unfulfilled request submitted by the NGO.
    """
    food_req = get_object_or_404(FoodRequest, pk=pk, receiver=request.user)

    if food_req.status not in ['PENDING']:
        messages.error(request, "Only pending requests can be cancelled. Once approved or dispatched, please contact the donor.")
        return redirect('requests:ngo_my_requests')

    if request.method == 'POST':
        food_req.status = 'CANCELLED'
        food_req.save()

        # If no other pending requests exist, restore donation to AVAILABLE
        donation = food_req.donation
        has_other_requests = donation.requests.filter(status__in=['PENDING', 'APPROVED']).exists()
        if not has_other_requests and donation.status == 'REQUESTED':
            donation.status = 'AVAILABLE'
            donation.save()

        messages.info(request, f"Your request for '{food_req.donation.food_name}' has been cancelled.")
        return redirect('requests:ngo_my_requests')

    context = {
        'food_request': food_req,
        'title': f"Cancel Request #{food_req.id}",
    }
    return render(request, 'requests/request_cancel_confirm.html', context)


# ==============================================================================
# DONOR INCOMING REQUEST MANAGEMENT VIEWS
# ==============================================================================

@donor_required
def donor_incoming_requests_view(request):
    """
    Lists incoming requests from NGOs for donations created by this donor.
    """
    status_filter = request.GET.get('status', 'PENDING')
    incoming = FoodRequest.objects.filter(
        donation__donor=request.user
    ).select_related('donation', 'receiver', 'receiver__profile', 'delivery')

    if status_filter != 'ALL':
        incoming = incoming.filter(status=status_filter)

    incoming = incoming.order_by('-requested_at')

    context = {
        'requests': incoming,
        'current_status': status_filter,
        'title': 'Incoming Food Requests',
    }
    return render(request, 'requests/donor_incoming_requests.html', context)


@donor_required
def donor_accept_request_view(request, pk):
    """
    Accept an incoming request from an NGO, creating or activating a Delivery task for volunteers.
    """
    food_req = get_object_or_404(FoodRequest, pk=pk, donation__donor=request.user)

    if food_req.status != 'PENDING':
        messages.warning(request, f"This request is already marked as {food_req.get_status_display()}.")
        return redirect('requests:donor_incoming_requests')

    if request.method == 'POST':
        food_req.status = 'APPROVED'
        food_req.save()

        # Update donation status
        donation = food_req.donation
        donation.status = 'ACCEPTED'
        donation.save()

        # Initialize delivery record for volunteers to claim
        delivery, created = Delivery.objects.get_or_create(
            food_request=food_req,
            defaults={'delivery_status': 'ASSIGNED'}
        )

        messages.success(
            request,
            f"You approved the request from '{food_req.receiver.profile.organization_name or food_req.receiver.username}'! "
            "A delivery task is now available for our volunteer team to pick up."
        )
        return redirect('requests:donor_incoming_requests')

    context = {
        'food_request': food_req,
        'title': f"Accept Request #{food_req.id}",
    }
    return render(request, 'requests/donor_request_action.html', {
        'action_type': 'accept',
        'food_request': food_req,
        'title': f"Confirm Acceptance: Request #{food_req.id}"
    })


@donor_required
def donor_reject_request_view(request, pk):
    """
    Reject an incoming food request from an NGO.
    """
    food_req = get_object_or_404(FoodRequest, pk=pk, donation__donor=request.user)

    if food_req.status != 'PENDING':
        messages.warning(request, f"This request is already marked as {food_req.get_status_display()}.")
        return redirect('requests:donor_incoming_requests')

    if request.method == 'POST':
        food_req.status = 'REJECTED'
        food_req.save()

        # Check if donation can be returned to AVAILABLE
        donation = food_req.donation
        has_other = donation.requests.filter(status__in=['PENDING', 'APPROVED']).exists()
        if not has_other:
            donation.status = 'AVAILABLE'
            donation.save()

        messages.info(request, f"Request #{food_req.id} was rejected. The food item remains open for other requests.")
        return redirect('requests:donor_incoming_requests')

    return render(request, 'requests/donor_request_action.html', {
        'action_type': 'reject',
        'food_request': food_req,
        'title': f"Confirm Rejection: Request #{food_req.id}"
    })


# ==============================================================================
# VOLUNTEER DISPATCH & DELIVERY VIEWS
# ==============================================================================

@volunteer_required
def volunteer_dashboard_view(request):
    """
    Volunteer Dashboard: Overview of assigned pickups, pending deliveries, and claimed tasks.
    """
    my_deliveries = Delivery.objects.filter(volunteer=request.user)
    
    active_deliveries_count = my_deliveries.filter(delivery_status__in=['ASSIGNED', 'PICKED_UP', 'IN_TRANSIT']).count()
    completed_deliveries_count = my_deliveries.filter(delivery_status='DELIVERED').count()
    
    # Available deliveries needing a volunteer
    open_tasks_count = Delivery.objects.filter(volunteer__isnull=True, delivery_status='ASSIGNED').count()

    my_active_tasks = my_deliveries.filter(
        delivery_status__in=['ASSIGNED', 'PICKED_UP', 'IN_TRANSIT']
    ).select_related('food_request', 'food_request__donation', 'food_request__receiver')[:5]

    available_tasks = Delivery.objects.filter(
        volunteer__isnull=True,
        delivery_status='ASSIGNED'
    ).select_related('food_request', 'food_request__donation', 'food_request__receiver')[:5]

    context = {
        'active_deliveries_count': active_deliveries_count,
        'completed_deliveries_count': completed_deliveries_count,
        'open_tasks_count': open_tasks_count,
        'my_active_tasks': my_active_tasks,
        'available_tasks': available_tasks,
        'title': 'Volunteer Dispatch Portal - Dashboard',
    }
    return render(request, 'requests/volunteer_dashboard.html', context)


@volunteer_required
def volunteer_deliveries_view(request):
    """
    View all open pickup opportunities and user's own active/completed deliveries.
    """
    tab = request.GET.get('tab', 'available')

    available_deliveries = Delivery.objects.filter(
        volunteer__isnull=True,
        delivery_status='ASSIGNED'
    ).select_related('food_request', 'food_request__donation', 'food_request__receiver', 'food_request__donation__donor')

    my_active = Delivery.objects.filter(
        volunteer=request.user,
        delivery_status__in=['ASSIGNED', 'PICKED_UP', 'IN_TRANSIT']
    ).select_related('food_request', 'food_request__donation', 'food_request__receiver', 'food_request__donation__donor')

    my_history = Delivery.objects.filter(
        volunteer=request.user,
        delivery_status='DELIVERED'
    ).select_related('food_request', 'food_request__donation', 'food_request__receiver', 'food_request__donation__donor').order_by('-delivery_time')

    context = {
        'available_deliveries': available_deliveries,
        'my_active': my_active,
        'my_history': my_history,
        'current_tab': tab,
        'title': 'Deliveries & Logistics Tasks',
    }
    return render(request, 'requests/volunteer_deliveries.html', context)


@volunteer_required
def volunteer_claim_delivery_view(request, pk):
    """
    Volunteer claims an unassigned delivery.
    """
    delivery = get_object_or_404(Delivery, pk=pk)

    if delivery.volunteer and delivery.volunteer != request.user:
        messages.warning(request, "This task has already been claimed by another volunteer.")
        return redirect('requests:volunteer_deliveries')

    if request.method == 'POST':
        delivery.volunteer = request.user
        delivery.delivery_status = 'ASSIGNED'
        delivery.save()
        messages.success(request, f"You have successfully claimed Delivery Task #{delivery.id}! Please proceed with collection.")
        return redirect('requests:volunteer_delivery_detail', pk=delivery.id)

    context = {
        'delivery': delivery,
        'title': f"Claim Delivery Task #{delivery.id}",
    }
    return render(request, 'requests/volunteer_claim_confirm.html', context)


@volunteer_required
def volunteer_delivery_detail_view(request, pk):
    """
    Detailed dispatch sheet with donor pickup contact, receiver delivery address,
    and actions to mark as collected or delivered.
    """
    delivery = get_object_or_404(
        Delivery.objects.select_related(
            'food_request',
            'food_request__donation',
            'food_request__donation__donor',
            'food_request__donation__donor__profile',
            'food_request__receiver',
            'food_request__receiver__profile',
            'volunteer'
        ),
        pk=pk
    )

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks', '').strip()

        if action == 'mark_collected':
            delivery.mark_picked_up(volunteer_user=request.user)
            if remarks:
                delivery.remarks = (delivery.remarks + f"\n[Pickup Note]: {remarks}").strip()
                delivery.save()
            messages.success(request, f"Food collection recorded! Status updated to 'In Transit'.")
            return redirect('requests:volunteer_delivery_detail', pk=delivery.id)

        elif action == 'mark_delivered':
            delivery.mark_delivered(remarks=remarks)
            messages.success(
                request,
                f"Heartiest congratulations! Delivery #{delivery.id} was successfully marked as completed. "
                "Thank you for stopping food waste and feeding the community!"
            )
            return redirect('requests:volunteer_deliveries')

        elif action == 'update_remarks':
            delivery.remarks = remarks
            delivery.save()
            messages.info(request, "Delivery log remarks updated.")
            return redirect('requests:volunteer_delivery_detail', pk=delivery.id)

    form = DeliveryStatusUpdateForm(instance=delivery)

    context = {
        'delivery': delivery,
        'form': form,
        'title': f"Delivery Dispatch #{delivery.id} Tracking",
    }
    return render(request, 'requests/volunteer_delivery_detail.html', context)
