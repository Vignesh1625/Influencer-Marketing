
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.influencer_dashboard, name='influencer_dashboard'),
    path('additional-details/', views.influencer_additional_details, name='influencer_additional_details'),
    path('profile/', views.influencer_profile, name='influencer_profile'),
]