import json

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from order.models import Order, OrderItem
from order.serializers import OrderSerializer
from product.models import Category, Product

User = get_user_model()


class OrderAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='bob', email='bob@ex.com')
        self.category_0 = Category.objects.create(name='notebook', slug='notebook')
        self.product_0 = Product.objects.create(name='ASUS Zenbook', slug='asus-zenbook',
                                                category=self.category_0,
                                                price=1000)
        self.product_1 = Product.objects.create(name='Apple MacBook', slug='apple-macbook',
                                                category=self.category_0,
                                                price=2000)
        self.order_0 = Order.objects.create(
            customer=self.user,
            first_name='bob',
            last_name='dylan',
            email='bob@ex.com',
            address='street',
            phone='123456',
            city='Minas Tirith',
        )

        self.order_1 = Order.objects.create(
            customer=self.user,
            first_name='bob',
            last_name='dylan',
            email='bob@ex.com',
            address='street',
            phone='123456',
            city='Minas Tirith',
        )

        for product in [self.product_0, self.product_1]:
            OrderItem.objects.create(order=self.order_0, product=product, quantity=2, price=product.price)
            OrderItem.objects.create(order=self.order_1, product=product, quantity=2, price=product.price)

        self.client.force_authenticate(user=self.user)

    def test_list(self):
        url = reverse('order-list')
        response = self.client.get(url)
        orders = Order.objects.filter(customer=self.user)
        serializer_data = OrderSerializer(orders, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_retrieve(self):
        url = reverse('order-detail', kwargs={'pk': self.order_1.pk})
        response = self.client.get(url)
        serializer_data = OrderSerializer(self.order_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        data_for_cart = json.dumps({'product_id': self.product_0.pk, 'quantity': 3})
        self.client.post(reverse('cart'), data=data_for_cart, content_type='application/json')

        url = reverse('order-list')
        data = {'first_name': 'bob',
                'last_name': 'dylan',
                'email': 'bob@ex.com',
                'address': 'street',
                'phone': '123456',
                'city': 'Minas Tirith', }
        data_for_order = json.dumps(data)
        response = self.client.post(url, data=data_for_order, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Order.objects.count(), 3)
        self.assertEqual(Order.objects.last().customer, self.user)
        self.assertEqual(OrderItem.objects.count(), 5)
        self.assertEqual(OrderItem.objects.filter(order=Order.objects.last()).count(), 1)
