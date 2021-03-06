# Generated by Django 2.2.7 on 2020-04-04 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0013_trip_email_template"),
    ]

    operations = [
        migrations.CreateModel(
            name="TripDocument",
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
                ("document", models.FileField(upload_to="documents/")),
            ],
        ),
    ]
