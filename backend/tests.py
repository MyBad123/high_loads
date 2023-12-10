from django.test import TestCase
from django.urls import reverse
from backend.models import Category, Product, CategoryForProduct


class TestProducts(TestCase):
    def test_get_product(self):
        category = Category.objects.create(name='category1')
        product = Product.objects.create(name='product1', about='about', price=100)
        CategoryForProduct.objects.create(category=category, product=product)

        request = self.client.post('/products')
        data = [{'id': 1, 'name': 'product1', 'about': 'about', 'price': 100, 'category': ['category1']}]

        self.assertEqual(data, request.json())

    def test_single_product(self):
        category = Category.objects.create(name='category1')
        product = Product.objects.create(name='product1', about='about', price=100)
        CategoryForProduct.objects.create(category=category, product=product)

        request = self.client.get('/product?id=1')
        data = {'id': 1, 'name': 'product1', 'about': 'about', 'price': 100, 'category': ['category1']}

        self.assertEqual(data, request.json())

