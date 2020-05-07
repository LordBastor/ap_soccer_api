# Generated by Django 2.2.7 on 2019-12-28 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0009_auto_20191228_1900"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tripinvitation",
            name="payment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="payments.Payment",
            ),
        ),
    ]
