# Generated by Django 3.1.4 on 2020-12-28 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("killtracker", "0003_tracker_color"),
    ]

    operations = [
        migrations.AddField(
            model_name="tracker",
            name="ping_groups",
            field=models.ManyToManyField(
                blank=True,
                default=None,
                help_text="Option to ping specific group members - ",
                related_name="_tracker_ping_groups_+",
                to="auth.Group",
                verbose_name="group pings",
            ),
        ),
        migrations.AlterField(
            model_name="tracker",
            name="ping_type",
            field=models.CharField(
                choices=[("PN", "(none)"), ("PH", "@here"), ("PE", "@everybody")],
                default="PN",
                help_text="Option to ping every member of the channel",
                max_length=2,
                verbose_name="channel pings",
            ),
        ),
    ]