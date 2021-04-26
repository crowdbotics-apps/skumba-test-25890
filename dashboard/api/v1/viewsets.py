from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dashboard.models.base import App, Plan, Subscription

from .serializers import AppSerializer, PlanSerializer, SubscriptionSerializer
from ...models import PlanNameChoices


class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all().order_by("-created_at")
    serializer_class = AppSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        name = request.data.get("name")
        description = request.data.get("description")
        app_type = request.data.get("type")
        framework = request.data.get("framework")
        domain_name = request.data.get("domain_name")
        user = request.user
        try:
            app = App.objects.create(
                name=name,
                description=description,
                type=app_type,
                framework=framework,
                domain_name=domain_name,
                user=user
            )
            plan, _ = Plan.objects.get_or_create(
                name=PlanNameChoices.FREE.value,
                description="Free"
            )
            user = request.user
            Subscription.objects.create(
                user=user,
                plan=plan,
                app=app
            )
            serializer = self.get_serializer(app)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        except Exception as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        try:
            App.objects.filter(id=pk).delete()
            return Response({"Message" "successfully deleted App"})
        except Exception as error:
            return Response({"Error": str(error)})

    def partial_update(self, request, pk):
        try:
            return super().partial_update(request, pk)
        except Exception as error:
            return Response(
                {"Error": str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all().order_by("-created_at")
    serializer_class = PlanSerializer
    permission_classes = (IsAuthenticated,)


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all().order_by("-created_at")
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
