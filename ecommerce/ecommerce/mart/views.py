
from django.shortcuts import render
from products.models import Product  

def mart(request):
    active_products = Product.objects.filter(active=True)
    return render(request, 'mart.html', {'products': active_products})

def cart(request):
    if request.method == 'POST':
        selected_product_ids = request.POST.getlist('selected_products')
        selected_products = Product.objects.filter(id__in=selected_product_ids, active=True)
        return render(request, 'cart.html', {'selected_products': selected_products})
    return render(request, 'cart.html', {'selected_products': []})
