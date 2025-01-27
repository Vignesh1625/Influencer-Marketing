# influencers/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import InfluencerInfo, InfluencerSocialMedia
from .forms import InfluencerAdditionalForm

from Products.views import get_influencer_products, get_influencer_requests

def get_influencer_id(request):
    return get_object_or_404(InfluencerInfo, user=request.user)

@login_required
@transaction.atomic  # Ensure both models are created in a single transaction
def influencer_additional_details(request):
    # Check if profile exists first
    if InfluencerInfo.objects.filter(user=request.user).exists():
        messages.info(request, "Your profile is already complete")
        return redirect('influencer_dashboard')

    if request.method == 'POST':
        form = InfluencerAdditionalForm(request.POST)
        if form.is_valid():
            try:
                # Create both models in a transaction
                influencer_info = InfluencerInfo.objects.create(
                    user=request.user,
                    full_name=form.cleaned_data['full_name'],
                    bio=form.cleaned_data['bio'],
                    base_amount=form.cleaned_data['base_amount'],
                    gender=form.cleaned_data['gender'],
                    location=form.cleaned_data['location']
                )
                
                social_media_details = InfluencerSocialMedia.objects.create(
                    user=request.user,
                    instagram_handle=form.cleaned_data['instagram_handle'],
                    instagram_followers=form.cleaned_data['instagram_followers'],
                    youtube_channel=form.cleaned_data['youtube_channel'],
                    youtube_subscribers=form.cleaned_data['youtube_subscribers']
                )
                
                messages.success(request, "Profile created successfully!")
                return redirect('influencer_dashboard')
            
            except Exception as e:
                messages.error(request, f"Error creating profile: {str(e)}")
    else:
        form = InfluencerAdditionalForm()
    
    return render(request, 'influencer/influencer_info.html', {'form': form})

@login_required
def influencer_dashboard(request):
    influencer = get_influencer_id(request)  # Using the local function
    if not influencer:
        messages.warning(request, "Please complete your profile first")
        return redirect('influencer_additional_details')
    
    try:
        my_products = get_influencer_products(request, influencer.user_id)
        new_requests = get_influencer_requests(request, influencer.user_id)
        
        return render(request, 'influencer/dashboard.html', {
            'influencer': influencer,
            'my_products': my_products,
            'new_requests': new_requests
        })
    
    except Exception as e:
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return render(request, 'influencer/dashboard.html', {
            'influencer': influencer,
            'my_products': [],
            'new_requests': []
        })

@login_required
def influencer_profile(request):
    influencer = get_influencer_id(request)
    if not influencer:
        messages.warning(request, "Please complete your profile first")
        return redirect('influencer_additional_details')
        
    try:
        social_media = InfluencerSocialMedia.objects.get(user=request.user)
        return render(request, 'influencer/influencer_profile.html', {
            'influencer': influencer,
            'social_media': social_media
        })
    except Exception as e:
        messages.error(request, f"Error loading profile: {str(e)}")
        return redirect('influencer_dashboard')

