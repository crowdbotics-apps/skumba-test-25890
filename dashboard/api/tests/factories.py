from factory import DjangoModelFactory, Faker, post_generation
from dashboard.models. import App

class AppFactory(DjangoModelFactory):
    class Meta:
        model = App