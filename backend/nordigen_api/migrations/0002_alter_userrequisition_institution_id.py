# Generated by Django 4.1.6 on 2023-02-05 11:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nordigen_api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userrequisition",
            name="institution_id",
            field=models.CharField(max_length=120),
        ),
    ]
