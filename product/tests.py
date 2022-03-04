import pdb
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from product.serializers import ProductSerializer
from product.models import Category, Product
from rest_framework.test import APIClient
from rest_framework import status


def sample_user(email='test@mail.com', password='Sstring1'):
    """Creste a sample user"""
    return get_user_model().objects.create_user(email, password)


def sample_product(title="My Product", price=1000, description="My product description"):
    raw_product = {
        'title': title,
        'price': price,
        'description': description,
    }
    return Product.objects.create(**raw_product)


def sample_category(title="My Category", slug="my_category", description="description"):
    raw_category = {
        'title': title,
        'slug': slug,
        'description': description
    }
    return Category.objects.create(**raw_category)


class ModelTests(TestCase):
    def test_product_creation_and_str(self):
        """Test that order is created and str is showed properly"""
        product1 = sample_product()
        self.assertIn(product1.title, str(product1))


class SerializerTests(TestCase):
    def test_product_serializer(self):
        """Test that order serializer"""
        product1 = sample_product()
        serialized_data = ProductSerializer(product1)
        data = serialized_data.data
        self.assertTrue(data['active'])
        self.assertIn('title', data)
        self.assertIn('price', data)


class PublicApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_product_list(self):
        """Test that products are retrieved porperly"""
        url = reverse('product-list', args=['v1'])
        for i in range(6):
            sample_product()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

    def test_get_category_list(self):
        """Test that products are retrieved porperly"""
        url = reverse('category-list', args=['v1'])
        for i in range(6):
            sample_category(slug=f'slug{i}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

    def test_create_new_category(self):
        """Test the creating new category"""
        url = reverse('category-list', args=['v1'])

        category_payload = {
            'title': 'title',
            'slug': 'slug123',
            'description': 'description'
        }
        response = self.client.post(url, category_payload)
        categories = Category.objects.all()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(categories.count(), 1)

    def test_create_new_products(self):
        """Test the product creation with categories"""
        url = reverse('product-list', args=['v1'])
        sample_category(slug='slug1')
        sample_category(slug='slug2')
        categories = Category.objects.all()
        product_payload = {
            'title': "My title",
            'description': 'Dumb description',
            'price': 1200,
            'category_ids': [cat.id for cat in categories]
        }

        response = self.client.post(url, product_payload)
        product_payload.update({'price': 1500})
        self.client.post(url, product_payload)
        products = Product.objects.all()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(products.count(), 2)
        self.assertEqual(products[0].category.count(), 2)
