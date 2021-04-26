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
    class Meta:
        model = Subscription
        fields = "__all__"
