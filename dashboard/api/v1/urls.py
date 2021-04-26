from django.urls import path
from .viewsets import AppViewSet

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
    )
]
