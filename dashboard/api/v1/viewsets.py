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
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as error:
            return Response(
                {"Error": str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )

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
    queryset = Subscription.objects.filter(active=True).order_by("-created_at")
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        plan_id = request.data.get("plan")
        app_id = request.data.get("app")
        active = request.data.get("active")
        plan = Plan.objects.get(id=plan_id)
        app = App.objects.get(id=app_id)
        user = request.user._wrapped if hasattr(
            request.user, '_wrapped') else request.user

        try:
            if app.subscription:
                subscription = app.subscription
                subscription.plan = plan
                subscription.active = active
                subscription.save()
            else:
                subscription = Subscription.objects.create(
                    app=app,
                    plan=plan,
                    user=user,
                    active=active
                )
            return Response(
                {
                    "app": subscription.app_id,
                    "plan": subscription.plan_id,
                    "user": subscription.user_id,
                    "active": subscription.active,
                    "created_at": subscription.created_at,
                    "updated_at": subscription.updated_at
                }, status=status.HTTP_201_CREATED
            )
        except Subscription.DoesNotExist:
            subscription = Subscription.objects.create(
                app=app.id,
                plan=plan.id,
                user=user.id
            )
            serializer = self.get_serializer(subscription)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )

    def destroy(self, request, pk):
        try:
            subscription = Subscription.objects.get(id=pk)
            subscription.soft_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
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
