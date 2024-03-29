# Generated by Django 5.0.1 on 2024-01-12 00:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_defect_reporter_name_alter_defect_solution_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="defect",
            name="reporter_name",
            field=models.CharField(
                help_text="Nom de la personne rapportant l'erreur",
                max_length=255,
                verbose_name="Nom",
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="type",
            field=models.CharField(
                choices=[
                    ("VTP", "VTP - Véhicule de Transport de Personnel"),
                    ("VL", "VL - Véhicule Léger"),
                    ("VPSP", "VPSP - Véhicule de Premiers Secours à Personnes"),
                    ("VTU", "VTU - Véhicule Tout Usage"),
                    ("VLTT", "VLTT - Véhicule Léger Tout Terrain"),
                    ("OTHER", "Autre"),
                ],
                max_length=255,
                verbose_name="type de véhicule",
            ),
        ),
    ]
