from django.db import models
from decimal import Decimal

class Order(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    region = models.CharField(max_length=3)
    date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order on {self.date} - Total: {self.total_price}"
