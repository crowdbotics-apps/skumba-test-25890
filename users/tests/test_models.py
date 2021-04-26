import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return UserFactory.build()


def test_user_get_absolute_url(user: settings.AUTH_USER_MODEL):
    print(type(user))
    assert user.get_absolute_url() == f"/users/{user.username}/"
