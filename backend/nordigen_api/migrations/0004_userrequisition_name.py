# Generated by Django 4.1.6 on 2023-02-05 14:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nordigen_api", "0003_userrequisition_reference_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="userrequisition",
            name="name",
            field=models.CharField(default="UNKNOWN", max_length=120),
        ),
    ]
