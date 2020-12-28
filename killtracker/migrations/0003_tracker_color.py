# Generated by Django 3.1.4 on 2020-12-28 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("killtracker", "0002_add_victim_ship_types"),
    ]

    operations = [
        migrations.AddField(
            model_name="tracker",
            name="color",
            field=models.CharField(
                blank=True,
                default=None,
                help_text="Optional color for embed on Discord",
                max_length=7,
                null=True,
            ),
        ),
    ]