from rest_framework import serializers

from dashboard.models import App, Plan, Subscription


class AppSerializer(serializers.ModelSerializer):
    name: str = serializers.CharField(
        max_length=50,
        min_length=1,
        required=True
    )
    description: str = serializers.CharField()
    type: str = serializers.CharField(required=True)
    framework: str = serializers.CharField(required=True)
    domain_name: str = serializers.CharField(max_length=50)

    class Meta:
        model = App
        fields = "__all__"


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "description", "price", "created_at",
                  "updated_at"]


class SubscriptionSerializer(serializers.ModelSerializer):
    app = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=App.objects.all()
    )
    plan = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Plan.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    active = serializers.BooleanField(required=True)

    class Meta:
        model = Subscription
        fields = [
            "id", "user", "plan", "app", "active", "created_at", "updated_at"
        ]
