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
            requests__influencer_id=influencer_id,  # Changed from productinfluencer to requests
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
        return NewMatches.objects.none()  # Changed from ProductInfluencer to NewMatches
    

def get_business_products(request, business_id):
    try:
        products = Product.objects.filter(business_id=business_id)
        return products if products else None
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return None
    



# Add these new views to Products/views.py
@login_required
def find_similar_influencers(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product.business.user != request.user:
        return HttpResponseForbidden("Permission denied")
    
    all_influencers = InfluencerInfo.objects.all()
    
    # # Prepare text for similarity analysis
    # product_text = product.description
    # influencer_bios = [inf.bio for inf in all_influencers]
    
    # if not influencer_bios:
    #     messages.info(request, "No influencers available for matching")
    #     return redirect('business_dashboard')
    
    # # Calculate TF-IDF similarity
    # vectorizer = TfidfVectorizer(stop_words='english')
    # tfidf_matrix = vectorizer.fit_transform([product_text] + influencer_bios)
    # cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    
    # # Get filtered influencers
    # similar_indices = [i for i, score in enumerate(cosine_sim[0]) if score > 0.1]
    # similar_influencers = [all_influencers[i] for i in similar_indices]
    
    # # Apply filters
    # location = request.GET.get('location')
    # gender = request.GET.get('gender')
    # min_price = request.GET.get('min_price')
    # max_price = request.GET.get('max_price')
    
    # filtered_influencers = similar_influencers
    # if location:
    #     filtered_influencers = [inf for inf in filtered_influencers if inf.location.lower() == location.lower()]
    # if gender:
    #     filtered_influencers = [inf for inf in filtered_influencers if inf.gender == gender]
    # if min_price:
    #     filtered_influencers = [inf for inf in filtered_influencers if inf.base_amount >= float(min_price)]
    # if max_price:
    #     filtered_influencers = [inf for inf in filtered_influencers if inf.base_amount <= float(max_price)]
    
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

