from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal, ROUND_HALF_UP
from .serializers import CalculationSerializer
from rest_framework.decorators import api_view
from .models import Order
from .serializers import OrderSerializer
from django.db.models import Q
from datetime import datetime


class CalculatePriceAPI(APIView):
    def post(self, request):
        serializer = CalculationSerializer(data=request.data)
        if serializer.is_valid():
            price = serializer.validated_data['price']
            quantity = serializer.validated_data['quantity']
            region = serializer.validated_data['region']

            # Calculate initial price before any discounts or VAT
            initial_price = Decimal(price) * Decimal(quantity)

            # Apply discount based on initial price
            if initial_price >= Decimal('50'):
                discount = initial_price * Decimal('0.15')
            elif initial_price >= Decimal('10'):
                discount = initial_price * Decimal('0.10')
            elif initial_price >= Decimal('7'):
                discount = initial_price * Decimal('0.07')
            elif initial_price >= Decimal('5'):
                discount = initial_price * Decimal('0.05')
            elif initial_price >= Decimal('1'):
                discount = initial_price * Decimal('0.03')
            else:
                discount = Decimal('0')

            price_with_discount = initial_price - discount

            # Apply VAT based on region
            vat_rates = {
                'uzb': Decimal('0.15'),
                'kaz': Decimal('0.20'),
                'geo': Decimal('0.12'),
                'ukr': Decimal('0.08'),
                'chn': Decimal('0.18'),
            }
            vat = price_with_discount * vat_rates.get(region, Decimal('0'))
            total_price = price_with_discount + vat

            # Round the prices to 2 decimal places
            initial_price = initial_price.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            price_with_discount = price_with_discount.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            total_price = total_price.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            # Save the order to the database
            order = Order(
                price=price,
                quantity=quantity,
                region=region,
                date=request.data.get('date', None),  # Set date if available
                total_price=total_price
            )
            order.save()

            # Return all calculated prices
            return Response({
                "initial_price": initial_price,
                "price_with_discount": price_with_discount,
                "total_price": total_price
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def list_orders(request):
    # Get optional filters from query parameters
    month = request.query_params.get('month')
    region = request.query_params.get('region')

    # Filter orders by month and region if provided
    orders = Order.objects.all()
    if month:
        # Convert month to a datetime object for filtering
        try:
            month_date = datetime.strptime(month, '%Y-%m')
            orders = orders.filter(date__year=month_date.year, date__month=month_date.month)
        except ValueError:
            return Response({"error": "Invalid month format. Use 'YYYY-MM'."}, status=400)

    if region:
        orders = orders.filter(region=region)

    # Serialize and return the filtered orders
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
