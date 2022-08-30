from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ('product', 'price', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = OrderItemSerializer(many=True, read_only=True)
    paid = serializers.BooleanField(read_only=True)

    class Meta:
        model = Order
        fields = ('id',
                  'customer',
                  'first_name',
                  'last_name',
                  'email',
                  'address',
                  'phone',
                  'city',
                  'postal_code',
                  'items',
                  'paid',)
