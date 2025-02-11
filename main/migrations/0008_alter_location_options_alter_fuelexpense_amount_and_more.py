# Generated by Django 5.1.4 on 2025-01-09 10:43

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_alter_fuelexpense_options_alter_fuelexpense_vehicle"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="location",
            options={"verbose_name": "Parking"},
        ),
        migrations.AlterField(
            model_name="fuelexpense",
            name="amount",
            field=models.DecimalField(
                decimal_places=2, max_digits=5, verbose_name="montant / €"
            ),
        ),
        migrations.AlterField(
            model_name="fuelexpense",
            name="quantity",
            field=models.DecimalField(
                decimal_places=2, max_digits=5, verbose_name="quantité / L"
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
