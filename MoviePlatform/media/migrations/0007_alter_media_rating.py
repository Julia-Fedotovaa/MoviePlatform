# Generated by Django 5.1.4 on 2025-01-06 20:46

import media.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0006_media_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='rating',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[media.validators.validate_rating]),
        ),
    ]
