from django.urls import path
from .views import CalculatePriceAPI, list_orders

urlpatterns = [
    path('api/calculate-price/', CalculatePriceAPI.as_view(), name='calculate-price-api'),
    path('api/orders/', list_orders, name='list-orders'),

]
