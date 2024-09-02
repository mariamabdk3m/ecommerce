from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product, Order, Transaction
from products.forms import OrderForm
import pandas as pd
import os

@login_required
def cart(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            selected_products = form.cleaned_data['products']
            
            user = request.user
            
            order = Order.objects.create(order_name="New Order", user=user)
            order.products.set(selected_products)
            order.save()

            transaction = Transaction.objects.create(transaction_order=order)

            file_path = 'excel_file.xlsx'
            if os.path.exists(file_path):
                df = pd.read_excel(file_path)
            else:
                df = pd.DataFrame(columns=['orderID', 'orderName', 'username', 'status'])

            next_order_id = df['orderID'].max() + 1 if not df.empty else 1
            
            df = df._append({
                'orderID': next_order_id,
                'orderName': order.order_name,
                'username': request.user.username,
                'status': 'Pending'  
            }, ignore_index=True)

            df.to_excel(file_path, index=False)

            return render(request, 'mart/cart.html', {'selected_products': selected_products})

    else:
        form = OrderForm()
    return render(request, 'cart.html', {'form': form, 'selected_products': []})


@login_required
def mart(request):
    active_products = Product.objects.filter(active=True)
    return render(request, 'mart/mart.html', {'products': active_products})

