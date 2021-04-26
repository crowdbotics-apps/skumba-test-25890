from typing import Callable

import pytest
from django.conf import settings
from rest_framework.test import APIRequestFactory, force_authenticate

from dashboard.api.tests.factories import AppFactory, PlanFactory, \
    SubscriptionFactory
from dashboard.api.v1.viewsets import AppViewSet, PlanViewSet, \
    SubscriptionViewSet
from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def request_factory():
    return APIRequestFactory()


@pytest.fixture
def user():
    return UserFactory.create()


@pytest.fixture
def app(user):
    return AppFactory.create(user=user)


@pytest.fixture
def plan():
    return PlanFactory.create()


@pytest.fixture
def susbscription(user, app, plan):
    return SubscriptionFactory.create(
        user=user,
        app=app,
        plan=plan
    )


@pytest.fixture
def apps_view():
    return AppViewSet.as_view({"post": "create", "get": "list"})


@pytest.fixture
def app_view():
    return AppViewSet.as_view(
        {
            "get": "retrieve",
            "delete": "destroy",
            "patch": "partial_update",
        }
    )


@pytest.fixture
def plans_view():
    return PlanViewSet.as_view({"get": "list"})


@pytest.fixture
def plan_view():
    return PlanViewSet.as_view({"get": "retrieve"})


@pytest.fixture
def subscriptions_view():
    return SubscriptionViewSet.as_view({"get": "list"})


@pytest.fixture
def subscription_view():
    return SubscriptionViewSet.as_view(
        {
            "get": "retrieve",
            "delete": "destroy",
            "patch": "partial_update",
        }
    )


def test_post_app(
        user: settings.AUTH_USER_MODEL,
        request_factory: APIRequestFactory,
        apps_view: Callable
):
    app_payload = {
        "name": "awesome",
        "description": "Very good",
        "type": "Web",
        "framework": "Django"
    }
    request = request_factory.post(
        "/api/v1/apps/",
        app_payload
    )
    force_authenticate(request, user=user)
    response = apps_view(request)
    assert response.status_code == 201
    assert response.data["name"] == app_payload["name"]


def test_list_apps(
        user: settings.AUTH_USER_MODEL,
        request_factory: APIRequestFactory,
        apps_view: Callable
):
    app = AppFactory.create(user=user)
    request = request_factory.get("/api/v1/apps/")
    force_authenticate(request, user=user)
    response = apps_view(request)
    assert response.data[0]["name"] == app.name
    assert response.data[0]["description"] == app.description
    assert len(response.data) == 1


def test_retrieve_app(
    app: AppFactory,
    user: settings.AUTH_USER_MODEL,
    request_factory: APIRequestFactory,
    app_view: Callable,
    plan: PlanFactory
):
    request = request_factory.get(f"/api/v1/apps/{app.id}")
    force_authenticate(request, user=user)
    response = app_view(request, pk=app.id)
    assert response.data["name"] == app.name
    assert response.data["id"] == app.id


def test_delete_app(
    app: AppFactory,
    user: settings.AUTH_USER_MODEL,
    request_factory: APIRequestFactory,
    app_view: Callable,
    plan: PlanFactory
):
    request = request_factory.delete(f"/api/v1/apps/{app.id}")
    force_authenticate(request, user=user)
    response = app_view(request, pk=app.id)
    assert response.status_code == 204


def test_partial_update_app(
    app: AppFactory,
    user: settings.AUTH_USER_MODEL,
    request_factory: APIRequestFactory,
    app_view: Callable,
    plan: PlanFactory
):
    app_payload = {
        "framework": "Django"
    }
    request = request_factory.patch(
        f"/api/v1/apps/{app.id}",
        app_payload
    )
    force_authenticate(request, user=user)
    response = app_view(request, pk=app.id)
    assert response.status_code == 200
    assert response.data["framework"] == app_payload["framework"]


def test_get_plans(
        user: settings.AUTH_USER_MODEL,
        request_factory: APIRequestFactory,
        plans_view: Callable
):
    request = request_factory.get("/api/v1/plans/")
    force_authenticate(request, user=user)
    response = plans_view(request)
    assert len(response.data) == 3


def test_get_plan(
        user: settings.AUTH_USER_MODEL,
        request_factory: APIRequestFactory,
        plan_view: Callable,
        plan: PlanFactory
):
    request = request_factory.get(f"/api/v1/plans/{plan.id}")
    force_authenticate(request, user=user)
    response = plan_view(request, pk=plan.id)
    assert response.data["name"] == plan.name
    assert response.data["id"] == plan.id


def test_get_subscriptions(
    user: settings.AUTH_USER_MODEL,
    subscriptions_view: Callable,
    susbscription: SubscriptionFactory,
    request_factory: APIRequestFactory,
):
    request = request_factory.get(f"/api/v1/subscriptions/")
    force_authenticate(request, user=user)
    response = subscriptions_view(request)
    assert len(response.data) == 1


def test_delete_subcription(
    user: settings.AUTH_USER_MODEL,
    subscription_view: Callable,
    susbscription: SubscriptionFactory,
    request_factory: APIRequestFactory,
):
    request = request_factory.delete(f"/api/v1/subscriptions"
                                     f"/{susbscription.id}")
    force_authenticate(request, user=user)
    response = subscription_view(request, pk=susbscription.id)
    assert response.status_code == 204


def test_partial_update_subcription(
    user: settings.AUTH_USER_MODEL,
    subscription_view: Callable,
    susbscription: SubscriptionFactory,
    request_factory: APIRequestFactory,
):
    susbscription_payload = {"active": False}
    request = request_factory.patch(
        f"/api/v1/subscriptions{susbscription.id}",
        susbscription_payload

    )
    force_authenticate(request, user=user)
    response = subscription_view(request, pk=susbscription.id)
    assert response.data["active"] == susbscription_payload["active"]
