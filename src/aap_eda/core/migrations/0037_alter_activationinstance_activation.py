# Generated by Django 3.2.18 on 2023-04-27 15:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0036_activationinstance_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activationinstance",
            name="activation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core.activation",
            ),
        ),
    ]
