from django.db import models


class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    orderName = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.orderName
