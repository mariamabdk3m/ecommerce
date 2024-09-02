import os
import pandas as pd
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from .forms import NewOrderForm, EditOrderForm
from products.models import Order
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views import View




@login_required
def user_orders_view(request):

    file_path = 'excel_file.xlsx'

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)

        user_orders = df[df['username'] == request.user.username].to_dict(orient='records')
    else:
        user_orders = []

    return render(request, 'tracking_system/user_orders.html', {'orders': user_orders})

def admin_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='/login/' 
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


@method_decorator(admin_required, name='dispatch')
class ExcelView(View):
    def get(self, request):
        file_path = 'excel_file.xlsx'

        if not os.path.exists(file_path):
            df = pd.DataFrame(columns=['orderID', 'orderName', 'username', 'status'])
            df = df._append({
                'orderID': 1,
                'orderName': 'Sample Order',
                'username': 'SampleUser',
                'status': 'Pending'
            }, ignore_index=True)

            df.to_excel(file_path, index=False)
        else:
            df = pd.read_excel(file_path)

        data = df.to_dict(orient='records')
        return render(request, './tracking_system/order_list.html', {'data': data})


@method_decorator(admin_required, name='dispatch')
class AddOrderView(View):
    form_class = NewOrderForm
    template_name = './tracking_system/add_order.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            file_path = 'excel_file.xlsx'

            if os.path.exists(file_path):
                df = pd.read_excel(file_path)
            else:
                df = pd.DataFrame(columns=['orderID', 'orderName', 'username', 'status'])

            next_order_id = df['orderID'].max() + 1 if not df.empty else 1

            df = df._append({
                'orderID': next_order_id,
                'orderName': form.cleaned_data['orderName'],
                'username': form.cleaned_data['username'],
                'status': form.cleaned_data['status']
            }, ignore_index=True)

            df.to_excel(file_path, index=False)
            return redirect('excel-view')

        return render(request, self.template_name, {'form': form})


@method_decorator(admin_required, name='dispatch')
class EditOrderView(View):
    template_name = "./tracking_system/edit_order.html"
    file_path = "excel_file.xlsx"

    def get(self, request, order_id):
        df = pd.read_excel(self.file_path)

        order = df[df['orderID'] == order_id].to_dict(orient='records')[0]
        form = EditOrderForm(initial=order)
        return render(request, self.template_name, {'form': form})

    def post(self, request, order_id):
        form = EditOrderForm(request.POST)
        if form.is_valid():
            df = pd.read_excel(self.file_path)
            df.loc[df['orderID'] == order_id, ['orderName', 'username', 'status']] = (
                form.cleaned_data['orderName'],
                form.cleaned_data['username'],
                form.cleaned_data['status']
            )


            df.to_excel(self.file_path, index=False)
            

            order = Order.objects.get(order_id=order_id)
            order.order_name = form.cleaned_data['orderName']
            order.user.username = form.cleaned_data['username']
            order.transaction.status = form.cleaned_data['status']
            order.save()
            order.transaction.save()

            return redirect('excel-view')

        return render(request, self.template_name, {'form': form})


@method_decorator(admin_required, name='dispatch')
class DeleteOrderView(View):
    def post(self, request, order_id):
        file_path = "excel_file.xlsx"
        df = pd.read_excel(file_path)
        df = df[df['orderID'] != order_id]
        df.to_excel(file_path, index=False)
        return redirect('excel-view')

@require_POST
@admin_required
def update_order_status(request, order_id):
    file_path = 'excel_file.xlsx'
    

    if not os.path.exists(file_path):
        return JsonResponse({"error": "Excel file not found"}, status=404)
    

    df = pd.read_excel(file_path)


    if order_id not in df['orderID'].values:
        return JsonResponse({"error": "Order not found"}, status=404)


    new_status = request.POST.get('status')
    if new_status:

        df.loc[df['orderID'] == order_id, 'status'] = new_status
        df.to_excel(file_path, index=False)
        return JsonResponse({"success": "Status updated successfully"})
    
    return JsonResponse({"error": "Invalid status or request"}, status=400)


@method_decorator(admin_required, name='dispatch')
class DeleteOrderView(View):
    def post(self, request, order_id):
        file_path = "excel_file.xlsx"
        df = pd.read_excel(file_path)


        df = df[df['orderID'] != order_id]
        df.to_excel(file_path, index=False)


        try:
            order = Order.objects.get(order_id=order_id)
            order.delete()
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        return JsonResponse({'message': 'Order deleted successfully'})
