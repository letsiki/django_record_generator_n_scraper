# Generated by Django 5.0.11 on 2025-03-19 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0003_alter_person_favorite_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='id_number',
            field=models.IntegerField(),
        ),
    ]
