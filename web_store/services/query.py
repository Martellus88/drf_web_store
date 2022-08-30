from rest_framework.generics import get_object_or_404

from order.models import Order, OrderItem
from payment.models import Wallet
from product.models import Product


def get_order_total_cost(order_id):
    order = get_object_or_404(Order, id=order_id)
    order_total_cost = order.get_total_cost()
    return order_total_cost


def change_order_paid(order_id):
    order = get_object_or_404(Order, id=order_id)
    order.paid = True
    order.save()


def get_user_wallet_wif_key(user):
    user_wif_key = Wallet.objects.get(user=user).wif_key
    return user_wif_key


def filter_order(**fields):
    return Order.objects.filter(**fields)


def create_order_item(**fields):
    OrderItem.objects.create(**fields)


def create_wallet(**fields):
    Wallet.objects.create(**fields)


def get_user_wallet(user_instance):
    return get_object_or_404(Wallet, user=user_instance)


def filter_product(**fields):
    return Product.objects.filter(**fields)


def get_product(**fields):
    return get_object_or_404(Product, **fields)
