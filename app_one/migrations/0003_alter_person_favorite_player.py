# Generated by Django 5.0.11 on 2025-03-19 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0002_remove_person_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='favorite_player',
            field=models.CharField(max_length=30),
        ),
    ]
