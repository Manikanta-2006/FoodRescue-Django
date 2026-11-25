"""
URL configuration for foodrescue project.
FoodRescue – Food Donation and Redistribution Management Platform
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Built-in Django Admin
    path('admin/', admin.site.urls),

    # Application URLs
    path('', include('donations.urls', namespace='donations')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('requests.urls', namespace='requests')),
]

# Custom Error Handlers
handler404 = 'donations.views_errors.custom_page_not_found'
handler500 = 'donations.views_errors.custom_server_error'

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
