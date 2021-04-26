from django.urls import path
from .viewsets import AppViewSet

urlpatterns = [
    path("apps/", AppViewSet.as_view(
        {"post": "create", "get": "list"}),
         name="app-create"),
]
