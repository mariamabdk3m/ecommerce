from django.http import JsonResponse
from django.views import View
from .models import Order
import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class OrderList(View):
    def get(self, request):
        orders = list(Order.objects.values())
        return JsonResponse(orders, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            order = Order.objects.create(
                orderName=data['orderName'],
                username=data['username'],
                status=data['status']
            )
            return JsonResponse({'orderID': order.orderID, 'orderName': order.orderName}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class OrderDetail(View):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
            return JsonResponse({
                'orderID': order.orderID,
                'orderName': order.orderName,
                'username': order.username,
                'status': order.status
            })
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

    def put(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
            data = json.loads(request.body)
            order.orderName = data.get('orderName', order.orderName)
            order.username = data.get('username', order.username)
            order.status = data.get('status', order.status)
            order.save()
            return JsonResponse({'message': 'Order updated successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

    def delete(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
            order.delete()
            return JsonResponse({'message': 'Order deleted successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
