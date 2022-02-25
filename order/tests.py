from django.contrib.auth import get_user_model
from django.test import TestCase
from product.models import Product
from order.models import Order


def sample_user(email='test@mail.com', password='Sstring1'):
    """Creste a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_order_creation_and_str(self):
        """Test that order is created and str is showed properly"""
        raw_product = {
            'title': "My Product",
            'price': 1000,
            'description': 'my description',
        }
        product1 = Product.objects.create(**raw_product)
        product2 = Product.objects.create(**raw_product)
        user = sample_user()
        raw_order = {
            # 'products': [product, product],
            'user': user
        }
        order = Order.objects.create(**raw_order)

        order.products.add(product1)
        order.products.add(product2)

        self.assertEqual(2, len(order.products.all()))
        self.assertIn(user.email, str(order))
        self.assertIn("2", str(order))
