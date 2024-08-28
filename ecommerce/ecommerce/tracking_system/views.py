from django.http import JsonResponse
from django.views import View
import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Simulated in-memory database
orders_db = {}
order_counter = 1  # Simulate auto-incrementing primary key

@method_decorator(csrf_exempt, name='dispatch')
class OrderList(View):
    def get(self, request):
        orders = list(orders_db.values())  # Convert dictionary values to a list
        return JsonResponse(orders, safe=False)

    def post(self, request):
        global order_counter
        try:
            data = json.loads(request.body)
            # Simulate auto-increment ID
            order_id = order_counter
            order_counter += 1
            
            # Create a new order entry
            orders_db[order_id] = {
                'orderID': order_id,
                'orderName': data['orderName'],
                'username': data['username'],
                'status': data['status']
            }
            return JsonResponse(orders_db[order_id], status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class OrderDetail(View):
    def get(self, request, order_id):
        try:
            order = orders_db[order_id]
            return JsonResponse(order)
        except KeyError:
            return JsonResponse({'error': 'Order not found'}, status=404)

    def put(self, request, order_id):
        try:
            data = json.loads(request.body)
            if order_id not in orders_db:
                return JsonResponse({'error': 'Order not found'}, status=404)
            
            # Update order details
            orders_db[order_id].update({
                'orderName': data.get('orderName', orders_db[order_id]['orderName']),
                'username': data.get('username', orders_db[order_id]['username']),
                'status': data.get('status', orders_db[order_id]['status'])
            })
            return JsonResponse({'message': 'Order updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, order_id):
        try:
            if order_id not in orders_db:
                return JsonResponse({'error': 'Order not found'}, status=404)

            del orders_db[order_id]
            return JsonResponse({'message': 'Order deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
