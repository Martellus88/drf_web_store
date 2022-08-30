from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APITestCase

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductAPITestCase(APITestCase):

    def setUp(self):
        self.category_0 = Category.objects.create(name='notebook', slug='notebook')
        self.category_1 = Category.objects.create(name='phone', slug='phone')
        self.product_0 = Product.objects.create(name='ASUS Zenbook', slug='asus-zenbook',
                                                category=self.category_0,
                                                price=1000)
        self.product_1 = Product.objects.create(name='Apple MacBook', slug='apple-macbook',
                                                category=self.category_0,
                                                price=2000)
        self.product_3 = Product.objects.create(name='Samsung Galaxy', slug='samsung-galaxy',
                                                category=self.category_1, price=500,
                                                description='like apple')

    def test_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        serializer_context = {
            'request': Request(response.wsgi_request),
        }
        products = Product.objects.all()
        serializer_data = ProductSerializer(products, many=True, context=serializer_context).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_retrieve(self):
        url = reverse('product-detail', kwargs={'slug': 'asus-zenbook'})
        response = self.client.get(url)
        serializer_context = {
            'request': Request(response.wsgi_request),
        }
        serializer_data = ProductSerializer(Product.objects.get(slug='asus-zenbook'),
                                            context=serializer_context).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_filter(self):
        url = reverse('product-list')
        response = self.client.get(url, data={'price': '1000'})
        serializer_context = {
            'request': Request(response.wsgi_request),
        }
        serializer_data = ProductSerializer(self.product_0, context=serializer_context).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([serializer_data], response.json())

    def test_search(self):
        url = reverse('product-list')
        response = self.client.get(url, data={'search': 'apple'})
        serializer_context = {
            'request': Request(response.wsgi_request),
        }
        serializer_data = ProductSerializer([self.product_1, self.product_3],
                                            many=True,
                                            context=serializer_context).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_ordering(self):
        url = reverse('product-list')
        response = self.client.get(url, data={'ordering': '-price'})
        serializer_context = {
            'request': Request(response.wsgi_request),
        }
        products = Product.objects.all().order_by('-price')
        serializer_data = ProductSerializer(products,
                                            many=True,
                                            context=serializer_context).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


class CategoryAPITestCase(APITestCase):

    def setUp(self):
        self.category_0 = Category.objects.create(name='notebook', slug='notebook')
        self.category_1 = Category.objects.create(name='phone', slug='phone')
        self.product_0 = Product.objects.create(name='ASUS Zenbook', slug='asus-zenbook',
                                                category=self.category_0,
                                                price=1000)
        self.product_1 = Product.objects.create(name='Apple MacBook', slug='apple-macbook',
                                                category=self.category_0,
                                                price=2000)
        self.product_3 = Product.objects.create(name='Samsung Galaxy', slug='samsung-galaxy',
                                                category=self.category_1, price=500,
                                                description='like apple')

    def test_list(self):
        url = reverse('category-list')
        response = self.client.get(url)
        serializer_context = {
            'request': Request(response.wsgi_request),
        }
        categories = Category.objects.all()
        serializer_data = CategorySerializer(categories, many=True, context=serializer_context).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_retrieve(self):
        url = reverse('category-detail', kwargs={'slug': 'notebook'})
        response = self.client.get(url)
        serializer_context = {
            'request': Request(response.wsgi_request),
        }
        serializer_data = CategorySerializer(Category.objects.get(slug='notebook'),
                                             context=serializer_context).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
