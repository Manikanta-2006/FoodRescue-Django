from django.shortcuts import render


def custom_page_not_found(request, exception=None):
    """
    Custom 404 Not Found error handler.
    """
    return render(request, '404.html', {'title': 'Page Not Found - FoodRescue'}, status=404)


def custom_server_error(request):
    """
    Custom 500 Server Error handler.
    """
    return render(request, '500.html', {'title': 'Internal Server Error - FoodRescue'}, status=500)
