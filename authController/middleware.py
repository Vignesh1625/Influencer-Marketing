# authController/middleware.py
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from .models import UserSession
from django.utils import timezone

class ProfileCompletionMiddleware:
    """
    Middleware to enforce profile completion for authenticated users.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Exclude paths that don't need profile checks
            excluded_paths = [
                reverse('login'),
                reverse('register'),
                reverse('logout'),
                reverse('business_client_info'),
                reverse('influencer_additional_details'),
                '/admin/',
            ]

            # Check if current path is excluded
            if request.path not in excluded_paths and not request.path.startswith('/admin/'):
                if request.user.role == 'BUSINESS':
                    from Business.models import BusinessClient
                    if not BusinessClient.objects.filter(user=request.user).exists():
                        messages.warning(request, "Please complete your business profile first")
                        return redirect('business_client_info')
                elif request.user.role == 'INFLUENCER':
                    from Influencer.models import InfluencerInfo
                    if not InfluencerInfo.objects.filter(user=request.user).exists():
                        messages.warning(request, "Please complete your influencer profile first")
                        return redirect('influencer_additional_details')

        response = self.get_response(request)
        return response

class SessionAuthMiddleware:
    """
    Middleware to validate session and CSRF token for authenticated users.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip validation for admin and auth pages
        if not request.path.startswith('/admin/') and not request.user.is_authenticated:
            session_id = request.COOKIES.get('session_id')
            csrf_token = request.META.get('HTTP_X_CSRFTOKEN', '')

            if session_id and csrf_token:
                try:
                    session = UserSession.objects.get(
                        session_id=session_id,
                        csrf_token=csrf_token,
                        expires_at__gt=timezone.now()
                    )
                    request.user = session.user
                except UserSession.DoesNotExist:
                    response = redirect('login')
                    response.delete_cookie('session_id')
                    return response

        response = self.get_response(request)
        return response