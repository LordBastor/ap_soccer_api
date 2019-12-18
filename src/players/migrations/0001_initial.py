# Generated by Django 2.2.7 on 2019-12-18 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_name', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('position', models.CharField(choices=[('Goalkeeper', 'Goalkeeper'), ('Defense', 'Defense'), ('Midfield', 'Midfield'), ('Forward', 'Forward')], max_length=10)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('country', models.CharField(default='United States', max_length=255)),
                ('zip_code', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('medical_conditions', models.TextField()),
                ('emergency_contact', models.CharField(max_length=255)),
            ],
        ),
    ]
