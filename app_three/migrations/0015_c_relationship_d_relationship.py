# Generated by Django 5.0.11 on 2025-03-21 18:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_three', '0014_dog'),
    ]

    operations = [
        migrations.AddField(
            model_name='c',
            name='relationship',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_three.dog'),
        ),
        migrations.AddField(
            model_name='d',
            name='relationship',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_three.dog'),
        ),
    ]
