from django.db import migrations
from dashboard.models.choices import PlanPriceChoices


def define_default_plans(apps, schema_editor):
    Plan = apps.get_model("dashboard.Plan")
    Plan.objects.all().delete()  # ensure no plans exist
    plans = [
        {
            "name": "Free",
            "description": "Free plan",
            "price": PlanPriceChoices.FREE.value,
        },
        {
            "name": "Standard",
            "description": "Standard plan",
            "price": PlanPriceChoices.STANDARD.value,
        },
        {
            "name": "Pro",
            "description": "Pro plan",
            "price": PlanPriceChoices.PRO.value,
        }
    ]
    for plan in plans:
        Plan.objects.create(**plan)


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_dashboard')
    ]

    operations = [
        migrations.RunPython(
            define_default_plans,
            migrations.RunPython.noop
        )
    ]