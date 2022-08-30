from django.conf import settings

from product.serializers import ProductSerializer

from services.query import filter_product, get_product


class Cart:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.cart = self.session.get(settings.CART_ID, {})

    def product_item_generator(self):
        products = filter_product(id__in=self.cart.keys())

        for product in products:
            self.cart[str(product.id)]['product'] = product
            self.cart[str(product.id)]['price'] = product.price

        for item in self.cart.values():
            yield item

    def add(self, product_id, quantity):
        product = get_product(id=product_id)
        product_id = str(product_id)
        serializer = ProductSerializer(product, context={'request': self.request})
        self.cart[product_id] = {'quantity': quantity, 'product': serializer.data}

        if self.cart[product_id]['quantity'] <= 0:
            del self.cart[product_id]
        self.save_session()

    def clear(self):
        self.session[settings.CART_ID] = {}
        self.session.modified = True

    def save_session(self):
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True
