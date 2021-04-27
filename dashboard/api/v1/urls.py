from django.http import JsonResponse
from django.urls import path

from .views import ping
from .viewsets import AppViewSet, PlanViewSet, SubscriptionViewSet


urlpatterns = [
    path("ping/", ping, name="ping"),
    path(
        "apps/",
        AppViewSet.as_view({"post": "create", "get": "list"}),
        name="app-create"
    ),
    path(
        'apps/<int:pk>/',
        AppViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy"
        })
    ),
    path(
        "subcriptions/",
        SubscriptionViewSet.as_view({"post": "create", "get": "list"}),
        name="app-create"
    ),
    path(
        'subcriptions/<int:pk>/',
        SubscriptionViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy"
        })
    ),
    path("plans/", PlanViewSet.as_view({"get": "list"})),
    path("plans/<int:pk>/", PlanViewSet.as_view({"get": "retrieve"}))
]
