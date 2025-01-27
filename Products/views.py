# products/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, ProductInfluencer, NewMatches
from django.shortcuts import get_object_or_404
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Influencer.models import InfluencerInfo
from django.http import HttpResponseForbidden
from django.db import transaction
from django.core.exceptions import ValidationError
# Create your views here.

import logging

logger = logging.getLogger(__name__)

@transaction.atomic
def add_product(request, business_id):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Get business or return 404
                business = get_object_or_404(BusinessClient, id=business_id)
                
                # Create product with form data
                product = Product.objects.create(
                    name=request.POST.get('name'),
                    description=request.POST.get('description'),
                    image=request.FILES.get('image'),
                    business=business
                )
                messages.success(request, f"Product {product.name} added successfully.")
                return redirect('products:product_list')
        except Exception as e:
            messages.error(request, f"Error creating product: {str(e)}")
            logger.error(f"Product creation failed: {str(e)}")
    return render(request, 'products/add_product.html')

def get_influencer_products(request, influencer_id):
    try:
        return Product.objects.filter(
            requests__influencer_id=influencer_id,
            requests__status='accepted'
        )
    except Exception as e:
        messages.error(request, f"Error getting influencer products: {str(e)}")
        return Product.objects.none()

def get_influencer_requests(request, influencer_id):
    try:
        return NewMatches.objects.filter(
            influencer_id=influencer_id,
            status='pending'
        )
    except Exception as e:
        messages.error(request, f"Error getting influencer requests: {str(e)}")
        return NewMatches.objects.none()
    

def get_business_products(request, business_id):
    try:
        products = Product.objects.filter(business_id=business_id)
        return products if products else None
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return None
    


@login_required
def find_similar_influencers(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product.business.user != request.user:
        return HttpResponseForbidden("Permission denied")
    
    all_influencers = InfluencerInfo.objects.all()
    
    context = {
        'product': product,
        'influencers': all_influencers,
        'filter_values': request.GET
    }
    return render(request, 'Products/similar_influencers.html', context)


@login_required
@transaction.atomic
def send_collaboration_request(request, product_id, influencer_id):
    try:
        with transaction.atomic():
            product = get_object_or_404(Product, id=product_id)
            influencer = get_object_or_404(InfluencerInfo, id=influencer_id)
            
            # Check permissions
            if product.business.user != request.user:
                return HttpResponseForbidden("Permission denied")
            
            # Create new match if doesn't exist
            match, created = NewMatches.objects.get_or_create(
                product=product,
                influencer=influencer,
                defaults={'status': 'pending'}
            )
            
            if created:
                messages.success(request, f"Request sent to {influencer.full_name}")
            else:
                messages.info(request, "Request already exists")
                
    except Exception as e:
        messages.error(request, f"Error sending request: {str(e)}")
        logger.error(f"Collaboration request failed: {str(e)}")
    
    return redirect('products:similar_influencers', product_id=product_id)

