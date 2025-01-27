# Product/urls.py

from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('add/<int:business_id>/', views.add_product, name='add_product'),
    path('similar-influencers/<int:product_id>/', views.find_similar_influencers, name='similar_influencers'),
    path('send-request/<int:product_id>/<int:influencer_id>/', views.send_collaboration_request, name='send_request'),
]

