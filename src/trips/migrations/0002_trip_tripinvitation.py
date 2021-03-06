# Generated by Django 2.2.7 on 2019-12-18 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TripInvitation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Trip",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("from_date", models.DateTimeField(blank=True)),
                ("to_date", models.DateTimeField(blank=True)),
                ("live", models.BooleanField(default=False)),
                ("player_price", models.DecimalField(decimal_places=2, max_digits=7)),
                ("traveler_price", models.DecimalField(decimal_places=2, max_digits=7)),
                ("package_options", models.ManyToManyField(to="trips.Package")),
            ],
        ),
    ]
