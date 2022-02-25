import factory
from product.models import Category, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Faker("pystr")
    slug = factory.Faker("pystr")
    description = factory.Faker("pystr")
    active = factory.Iterator([True, False])


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    price = factory.Faker("pyint")
    slug = factory.LazyAttribute(CategoryFactory)
    title = factory.Faker("pystr")

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.category.add(category)
