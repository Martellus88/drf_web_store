from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import OrderSerializer
from services.query import filter_order, create_order_item
from cart.cart import Cart
from .tasks import send_mail_order_created


class OrderAPIView(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   mixins.CreateModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return filter_order(customer=self.request.user.id)

    def perform_create(self, serializer):
        order = serializer.save()
        cart = Cart(self.request)
        for item in cart.product_item_generator():
            create_order_item(order=order, **item)
        cart.clear()
        send_mail_order_created.delay(order.first_name, order.id, order.email)
