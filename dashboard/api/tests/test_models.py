import pytest
from users.tests.factories import UserFactory
from .factories import AppFactory, PlanFactory, SubscriptionFactory
from dashboard.models.choices import PlanPriceChoices, PlanNameChoices


pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return UserFactory.create()


@pytest.fixture
def app(user):
    return AppFactory(user=user)


@pytest.fixture
def subscription(app):
    return SubscriptionFactory(
        app=app,
        plan=PlanFactory.create(),
        user=UserFactory.create()
    )


def test_plan_creation():
    plan = PlanFactory(name=PlanNameChoices.FREE.value, description="free",
                       price=PlanPriceChoices.FREE.value)
    assert plan.price == "$0"
    assert plan.name == "Free"


def test_subscription_creation(subscription):
    assert subscription.plan.price == PlanPriceChoices.FREE.value
