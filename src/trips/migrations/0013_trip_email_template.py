# Generated by Django 2.2.7 on 2020-04-04 12:15

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0012_auto_20191228_2052"),
    ]

    operations = [
        migrations.AddField(
            model_name="trip",
            name="email_template",
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
