import factory
from django.contrib.auth import get_user_model
from order.models import Order


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Faker("pystr")
    username = factory.Faker("pystr")


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def product(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for product in extracted:
                self.product.add(product)
