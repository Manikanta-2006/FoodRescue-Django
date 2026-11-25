from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    # NGO Routes
    path('ngo/dashboard/', views.ngo_dashboard_view, name='ngo_dashboard'),
    path('requests/create/<int:donation_id>/', views.request_food_view, name='request_food'),
    path('ngo/requests/', views.ngo_my_requests_view, name='ngo_my_requests'),
    path('ngo/requests/<int:pk>/cancel/', views.ngo_cancel_request_view, name='ngo_cancel_request'),

    # Donor Review Incoming Requests
    path('donor/requests/', views.donor_incoming_requests_view, name='donor_incoming_requests'),
    path('donor/requests/<int:pk>/accept/', views.donor_accept_request_view, name='donor_accept_request'),
    path('donor/requests/<int:pk>/reject/', views.donor_reject_request_view, name='donor_reject_request'),

    # Volunteer Routes
    path('volunteer/dashboard/', views.volunteer_dashboard_view, name='volunteer_dashboard'),
    path('volunteer/deliveries/', views.volunteer_deliveries_view, name='volunteer_deliveries'),
    path('volunteer/deliveries/<int:pk>/claim/', views.volunteer_claim_delivery_view, name='volunteer_claim_delivery'),
    path('volunteer/deliveries/<int:pk>/', views.volunteer_delivery_detail_view, name='volunteer_delivery_detail'),
]
