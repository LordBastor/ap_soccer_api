# Generated by Django 2.2.13 on 2021-06-20 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0027_auto_20210315_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='deposit_files',
            field=models.ManyToManyField(blank=True, related_name='deposit_files', to='trips.TripDocument'),
        ),
    ]
