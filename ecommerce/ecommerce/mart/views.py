from django.shortcuts import render, redirect

PRODUCTS = [
    {'id': 1, 'name': 'Cheese', 'price': 600},
    {'id': 2, 'name': 'Salami', 'price': 750},
    {'id': 3, 'name': 'Meat', 'price': 1200},
]

def mart(request):
    return render(request, 'mart.html', {'products': PRODUCTS})

def cart(request):
    if request.method == 'POST':
        selected_products = request.POST.getlist('selected_products')
        return render(request, 'cart.html', {'selected_products': selected_products})
    return render(request, 'cart.html', {'selected_products': []})
