import pytest
from factory.django import DjangoModelFactory
from dashboard.models.base import App, Plan, Subscription
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class AppFactory(DjangoModelFactory):
    name = "name"
    description = "description"
    type = "Web"
    framework = "Django"
    domain_name = "yourdomain"
    screenshot = "http://example.com"

    class Meta:
        model = App


class PlanFactory(DjangoModelFactory):
    name = "name"
    description = "description"

    class Meta:
        model = Plan


class SubscriptionFactory(DjangoModelFactory):

    class Meta:
        model = Subscription
