# Generated by Django 2.2.7 on 2019-12-18 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0004_auto_20191218_1406"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trip",
            name="from_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="trip",
            name="to_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
