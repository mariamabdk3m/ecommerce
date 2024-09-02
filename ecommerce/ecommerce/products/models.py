from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images/', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Mart Product'
        ordering = ['price']


class Order(models.Model):
    order_name = models.CharField(max_length=100)
    order_id = models.AutoField(primary_key=True)
    products = models.ManyToManyField(Product, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')  # Add this line

    def __str__(self):
        return f"Order {self.order_id}: {self.order_name}"

class Transaction(models.Model):
    transaction_order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='transaction')
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')  # Add this line

    def __str__(self):
        return f"Transaction for Order {self.transaction_order.order_id}"
