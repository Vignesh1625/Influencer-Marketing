from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.business_dashboard, name='business_dashboard'),
    path('client-info/', views.business_client_info, name='business_client_info'),
    path('profile/', views.business_profile, name='business_profile'),
    path('add-product/', views.add_product, name='add_product'),
]
