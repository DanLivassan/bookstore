from random import randint
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from order.serializers import OrderSerializer
from product.models import Product
from order.models import Order
from rest_framework import status
from rest_framework.test import APIClient
MAX_PER_PAGE = 5


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


def sample_order(user, products):
    raw_order = {
        # 'products': [product, product],
        'user': user
    }
    order = Order.objects.create(**raw_order)
    for product in products:
        order.products.add(product)
    return order


class ModelTests(TestCase):
    def test_order_creation_and_str(self):
        """Test that order is created and str is showed properly"""
        product1 = sample_product()
        product2 = sample_product()
        user = sample_user()
        order = sample_order(user, [product1, product2])
        self.assertEqual(2, len(order.products.all()))
        self.assertIn(user.email, str(order))
        self.assertIn("2", str(order))


class SerializerTests(TestCase):
    def test_order_serializer(self):
        """Test that order serializer"""
        product1 = sample_product()
        product2 = sample_product()
        user = sample_user()
        order = sample_order(user, [product1, product2])
        serialized_data = OrderSerializer(order)
        data = serialized_data.data
        self.assertEqual(len(data['products']), 2)
        self.assertEqual(data['total'], 2000)


class PublicApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_that_write_methods_fails(self):
        """Test if unauthenticated user perform write methods fails"""
        url = reverse('product-list', args=['v1'])
        post_response = self.client.post(url, {})
        put_response = self.client.put(url, {})
        patch_response = self.client.patch(url, {})

        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         post_response.status_code)
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         put_response.status_code)
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         patch_response.status_code)

    def test_get_order_list(self):
        """Test that orders are retrieved porperly and if the sum of prices matches with sum of products price"""
        url = reverse('order-list', args=['v1'])
        total = 0
        products = []
        for i in range(5):
            price = randint(1000, 2000)
            total += price
            products.append(sample_product(price=price))
        user = sample_user()
        sample_order(user=user, products=products)
        response = self.client.get(url)
        api_order = response.data['results'][0]

        self.assertEqual(api_order['total'], total)
        self.assertEqual(len(api_order['products']), 5)


class PrivateApiTest(TestCase):
    def setUp(self) -> None:
        self.user = sample_user(email='authenticated@mail.com')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_a_new_order(self):
        """Test that an order are created porperly"""
        url = reverse('order-list', args=['v1'])
        sample_product()
        sample_product()
        products = Product.objects.all()
        user = sample_user()
        order_payload = {
            'user': user.id,
            'products_ids': [p.id for p in products]
        }
        response = self.client.post(url, order_payload)
        orders = Order.objects.all()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders[0].products.count(), 2)
