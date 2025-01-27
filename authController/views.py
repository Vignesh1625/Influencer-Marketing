# authController/views.py
import uuid
import secrets
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from .forms import LoginForm, RegistrationForm
from .models import User, PasswordResetOTP, UserSession

# Helper function to check if a business profile exists
def check_business_profile_exists(user):
    """Check if the business user has completed their profile."""
    if user.role == 'BUSINESS':
        from Business.models import BusinessClient
        return BusinessClient.objects.filter(user=user).exists()
    return True

# Helper function to check if an influencer profile exists
def check_influencer_profile_exists(user):
    """Check if the influencer has completed their profile."""
    if user.role == 'INFLUENCER':
        from Influencer.models import InfluencerInfo
        return InfluencerInfo.objects.filter(user=user).exists()
    return True

# Decorator to validate session cookies and CSRF tokens
def cookie_based_redirect(view_func):
    """
    Decorator to validate session cookies and CSRF tokens.
    If valid, logs the user in and redirects to the dashboard.
    If invalid, redirects to the login page and clears cookies.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
            
        session_id = request.COOKIES.get('session_id')
        csrf_token = request.COOKIES.get('csrf_token')
        
        if session_id and csrf_token:
            try:
                # Validate session against the database
                session = UserSession.objects.get(
                    session_id=session_id,
                    csrf_token=csrf_token,
                    expires_at__gt=timezone.now()
                )
                login(request, session.user)  # Log the user in
                return redirect('dashboard')
                    
            except UserSession.DoesNotExist:
                # Invalid session, clear cookies and redirect to login
                messages.warning(request, "Session expired or invalid")
                response = redirect('login')
                response.delete_cookie('session_id')
                response.delete_cookie('csrf_token')
                return response
            
        return view_func(request, *args, **kwargs)
    return wrapper

# Login view with session and CSRF token handling
@cookie_based_redirect
def login_view(request):
    """
    Handles user login. On successful login:
    - Creates a new session with a UUID and CSRF token.
    - Stores the session in the database.
    - Sets secure cookies for session and CSRF token.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Delete any existing sessions for this user
            UserSession.objects.filter(user=user).delete()
            
            # Generate a new session UUID and CSRF token
            session_id = str(uuid.uuid4())
            csrf_token = secrets.token_hex(32)
            expires_at = timezone.now() + timezone.timedelta(seconds=settings.SESSION_COOKIE_AGE)
            
            # Create or update the session record in the database
            UserSession.objects.update_or_create(
                user=user,
                defaults={
                    'session_id': session_id,
                    'csrf_token': csrf_token,
                    'expires_at': expires_at
                }
            )

            # Prepare the response and set secure cookies
            if user.role == 'BUSINESS':
                if check_business_profile_exists(user):
                    response = redirect('business_dashboard')
                else:
                    response = redirect('business_client_info')
            else:
                if check_influencer_profile_exists(user):
                    response = redirect('influencer_dashboard')
                else:
                    response = redirect('influencer_additional_details')
            
            response.set_cookie(
                key='session_id',
                value=session_id,
                max_age=settings.SESSION_COOKIE_AGE,
                secure=not settings.DEBUG,
                httponly=True,
                samesite='Lax'
            )
            response.set_cookie(
                key='csrf_token',
                value=csrf_token,
                max_age=settings.SESSION_COOKIE_AGE,
                secure=not settings.DEBUG,
                samesite='Lax'
            )
            return response
            
        messages.warning(request, "Failed login attempt")
    else:
        form = LoginForm()

    return render(request, 'authController/login.html', {'form': form})

# Registration view with session creation
def register_view(request):
    """Handles user registration without cookie validation."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Authenticate and login user
            authenticated_user = authenticate(
                request,
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            
            if authenticated_user:
                login(request, authenticated_user)
                
                # Create session immediately after login
                session_id = str(uuid.uuid4())
                csrf_token = secrets.token_hex(32)
                expires_at = timezone.now() + timezone.timedelta(seconds=settings.SESSION_COOKIE_AGE)
                
                # Create new session record
                UserSession.objects.create(
                    user=authenticated_user,
                    session_id=session_id,
                    csrf_token=csrf_token,
                    expires_at=expires_at
                )
                
                # Set up response with proper redirect
                if authenticated_user.role == 'BUSINESS':
                    response = redirect('business_client_info')
                else:
                    response = redirect('influencer_additional_details')
                
                # Set cookies before returning response
                response.set_cookie(
                    'session_id',
                    session_id,
                    max_age=settings.SESSION_COOKIE_AGE,
                    secure=not settings.DEBUG,
                    httponly=True,
                    samesite='Lax'
                )
                response.set_cookie(
                    'csrf_token',
                    csrf_token,
                    max_age=settings.SESSION_COOKIE_AGE,
                    secure=not settings.DEBUG,
                    samesite='Lax'
                )
                return response
                
    else:
        form = RegistrationForm()
    
    return render(request, 'authController/register.html', {'form': form})

# Logout view with session cleanup
def logout_view(request):
    """
    Handles user logout. On logout:
    - Deletes the session from the database.
    - Clears session and CSRF cookies.
    - Flushes the session data.
    """
    if request.user.is_authenticated:
        # Delete all sessions for the user
        UserSession.objects.filter(user=request.user).delete()
        messages.info(request, f"User {request.user.email} logged out")
    
    # Prepare the response and clear cookies
    response = redirect('login')
    response.delete_cookie('session_id')
    response.delete_cookie('csrf_token')
    request.session.flush()
    return response

# Forgot password view with OTP generation
def forgot_password(request):
    """
    Handles password reset initiation. On submission:
    - Generates a 6-digit OTP.
    - Sends the OTP via email.
    - Stores the OTP in the database with an expiration time.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Generate a secure 6-digit OTP
            otp = secrets.randbelow(900000) + 100000
            otp_code = str(otp)
            
            # Delete any existing OTPs for this user
            PasswordResetOTP.objects.filter(user=user).delete()
            
            # Create a new OTP record (valid for 15 minutes)
            expires_at = timezone.now() + timezone.timedelta(minutes=15)
            PasswordResetOTP.objects.create(
                user=user,
                otp=otp_code,
                expires_at=expires_at
            )
            
            # Send the OTP via email
            send_mail(
                subject='Password Reset OTP',
                message=f'Your OTP for password reset is: {otp_code}\nValid for 15 minutes.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            # Store user ID in session for verification
            request.session['reset_user_id'] = str(user.id)
            return redirect('verify_otp')
            
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address')
    
    return render(request, 'authController/forgot_password.html')

# OTP verification view
def verify_otp(request):
    """
    Handles OTP verification. On successful verification:
    - Marks the OTP as verified in the session.
    - Redirects to the password reset page.
    """
    user_id = request.session.get('reset_user_id')
    
    if not user_id:
        messages.error(request, 'Invalid reset request')
        return redirect('login')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid user')
        return redirect('login')
    
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        
        try:
            otp_record = PasswordResetOTP.objects.get(user=user, otp=otp_entered)
            
            if timezone.now() > otp_record.expires_at:
                messages.error(request, 'OTP has expired')
                return redirect('verify_otp')
                
            # OTP verified - allow password reset
            request.session['verified_otp'] = True
            return redirect('reset_password')
            
        except PasswordResetOTP.DoesNotExist:
            messages.error(request, 'Invalid OTP')
    
    return render(request, 'authController/verify_otp.html')

# Password reset view
def reset_password(request):
    """
    Handles password reset after OTP verification. On submission:
    - Updates the user's password.
    - Cleans up OTP records and session data.
    """
    user_id = request.session.get('reset_user_id')
    otp_verified = request.session.get('verified_otp')
    
    if not user_id or not otp_verified:
        messages.error(request, 'Invalid reset request')
        return redirect('login')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid user')
        return redirect('login')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('reset_password')
            
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters')
            return redirect('reset_password')
            
        # Update the user's password
        user.set_password(password)
        user.save()
        
        # Cleanup OTP records and session data
        PasswordResetOTP.objects.filter(user=user).delete()
        del request.session['reset_user_id']
        del request.session['verified_otp']
        
        messages.success(request, 'Password updated successfully! Please login')
        return redirect('login')
    
    return render(request, 'authController/reset_password.html')