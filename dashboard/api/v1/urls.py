from django.urls import path
from .viewsets import AppViewSet, PlanViewSet

urlpatterns = [
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
    path("plans/", PlanViewSet.as_view({"get": "list"})),
    path("plans/<int:pk>/", PlanViewSet.as_view({"get": "retrieve"}))
]
