from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BusinessClientForm
from .models import BusinessClient
from Products.forms import ProductForm

@login_required
def business_client_info(request):
    try:
        business_client = BusinessClient.objects.filter(user=request.user).first()
        is_update = bool(business_client)
    except Exception:
        business_client = None
        is_update = False

    if request.method == 'POST':
        form = BusinessClientForm(request.POST, instance=business_client)
        if form.is_valid():
            try:
                business_client = form.save(commit=False)
                business_client.user = request.user
                business_client.save()
                messages.success(request, "Business profile saved successfully!")
                return redirect('business_dashboard')
            except Exception as e:
                messages.error(request, f"Error saving data: {e}")
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = BusinessClientForm(instance=business_client)

    return render(request, 'Business/business_client_info.html', {'form': form, 'is_update': is_update})


@login_required
def business_dashboard(request):
    business_client = get_object_or_404(BusinessClient, user=request.user)
    return render(request, 'Business/dashboard.html', {
        'business_client': business_client,
        'business_id': business_client.id
    })


@login_required
def business_profile(request):
    business_client = get_object_or_404(BusinessClient, user=request.user)
    return render(request, 'Business/business_profile.html', {'business_client': business_client})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            business_client = get_object_or_404(BusinessClient, user=request.user)
            product = form.save(commit=False)
            product.business = business_client
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('business_dashboard')
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = ProductForm()

    return render(request, 'Business/add_product.html', {'form': form})
