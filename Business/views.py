# Business/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BusinessClientForm
from .models import BusinessClient
from Products.forms import ProductForm

@login_required
def business_client_info(request):
    """
    View to handle business client profile creation and updates.
    Also ensures proper session tracking.
    """

    try:
        business_client = BusinessClient.objects.get(user=request.user)
        is_update = True
    except BusinessClient.DoesNotExist:
        business_client = None
        is_update = False

    if request.method == 'POST':
        form = BusinessClientForm(request.POST, instance=business_client)
        if form.is_valid():
            try:
                business_client = form.save(commit=False)
                business_client.user = request.user.id
                business_client.save()
                messages.success(request, "Business profile saved successfully!")
                return redirect('business_dashboard')
            except Exception as e:
                print("Error saving business client:", str(e))
                messages.error(request, f"Error saving data: {str(e)}")
        else:
            print("Form errors:", form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        form = BusinessClientForm(instance=business_client)

    return render(request, 'Business/business_client_info.html', {
        'form': form,
        'is_update': is_update
    })

@login_required
def business_dashboard(request):
    """
    View to display the business dashboard with UUID handling.
    """
    try:
        business_client = BusinessClient.objects.select_related('user').get(user=request.user)
        return render(request, 'Business/dashboard.html', {
            'business_client': business_client,
            'business_id': business_client.id  
        })
    except BusinessClient.DoesNotExist:
        messages.warning(request, "Please complete your business profile first.")
        return redirect('business_client_info')


@login_required
def business_profile(request):
    try:
        
        business = BusinessClient.objects.get(user = request.user.id)
        print(business)
        return render(request, 'Business/business_profile.html', {'business': business})
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('business_dashboard')
    
@login_required
def add_product(request):
    """
    View to add a product with proper UUID handling.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                business_client = BusinessClient.objects.get(user=request.user)
                product = form.save(commit=False)
                product.business = business_client  # Direct assignment of instance
                product.save()
                messages.success(request, "Product added successfully!")
                return redirect('business_dashboard')
            except BusinessClient.DoesNotExist:
                messages.error(request, "Business profile not found.")
                return redirect('business_client_info')
    else:
        form = ProductForm()
    
    return render(request, 'Business/add_product.html', {'form': form})