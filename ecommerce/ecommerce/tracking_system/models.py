from django.db import models

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    orderName = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=[
            ('requested', 'Requested'),
            ('preparing', 'Preparing'),
            ('delivering', 'Delivering'),
            ('delivered', 'Delivered')
        ],
        default='requested'
    )

    def __str__(self):
        return self.orderName
