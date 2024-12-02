from rest_framework import serializers
from .models import Order
from decimal import Decimal

class CalculationSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    quantity = serializers.IntegerField(min_value=1)
    region = serializers.ChoiceField(choices=[
        ('uzb', 'Uzbekistan'),
        ('kaz', 'Kazakhstan'),
        ('geo', 'Georgia'),
        ('ukr', 'Ukraine'),
        ('chn', 'China'),
    ])
    date = serializers.DateField(required=False)  # Optional field if date is needed but not used in calculation

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['price', 'quantity', 'region', 'date', 'total_price']