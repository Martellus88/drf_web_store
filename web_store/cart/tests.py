import json

from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APITestCase

from product.models import Category, Product
from product.serializers import ProductSerializer


class CartAPITestCase(APITestCase):

    def setUp(self):
        self.category_0 = Category.objects.create(name='notebook', slug='notebook')
        self.product_0 = Product.objects.create(name='ASUS Zenbook', slug='asus-zenbook',
                                                category=self.category_0,
                                                price=1000)

    def test_add_to_cart(self):
        data = json.dumps({'product_id': 1, 'quantity': 3})
        url = reverse('cart')
        response = self.client.post(url, data=data, content_type='application/json')
        serializer_context = {
            'request': Request(response.wsgi_request),
        }
        product_serializer_data = ProductSerializer(self.product_0, context=serializer_context).data
        expected_data = {'1': {'quantity': 3, 'product': product_serializer_data}}
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)

    def test_get_empty_cart(self):
        url = reverse('cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})

    def test_get_not_empty_cart(self):
        url = reverse('cart')
        data = json.dumps({'product_id': self.product_0.pk, 'quantity': 3})
        self.client.post(url, data=data, content_type='application/json')
        response = self.client.get(url)
        serializer_context = {
            'request': Request(response.wsgi_request),
        }
        product_serializer_data = ProductSerializer(self.product_0, context=serializer_context).data
        expected_data = {str(self.product_0.pk): {'quantity': 3, 'product': product_serializer_data}}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
