from django.urls import path, re_path
from . import views

app_name = 'donations'

urlpatterns = [
    # Public Pages
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('how-it-works/', views.how_it_works_view, name='how_it_works'),
    path('contact/', views.contact_view, name='contact'),
    path('donations/', views.donation_list_view, name='donation_list'),

    # Academic Requirement: slug converter
    path('donations/detail/<slug:slug>/', views.donation_detail_slug_view, name='donation_detail_slug'),

    # Academic Requirement: int converter
    path('donations/id/<int:pk>/', views.donation_detail_id_view, name='donation_detail_id'),

    # Academic Requirement: re_path regex pattern
    re_path(r'^donations/category/(?P<category_code>[a-zA-Z0-9_-]+)/$', views.donation_category_view, name='donation_by_category'),

    # Academic Requirement: JsonResponse endpoints
    path('api/donations/', views.api_donations_json_view, name='api_donations'),
    path('api/stats/', views.api_stats_json_view, name='api_stats'),

    # Donor Management Routes
    path('donor/dashboard/', views.donor_dashboard_view, name='donor_dashboard'),
    path('donor/donations/create/', views.donor_add_donation_view, name='donor_add_donation'),
    path('donor/donations/', views.donor_my_donations_view, name='donor_my_donations'),
    path('donor/donations/<int:pk>/edit/', views.donor_edit_donation_view, name='donor_edit_donation'),
    path('donor/donations/<int:pk>/delete/', views.donor_delete_donation_view, name='donor_delete_donation'),

    # Admin Platform Overview
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
]
