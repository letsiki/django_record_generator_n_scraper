# Generated by Django 5.0.11 on 2025-03-21 11:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_three', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuisine', models.CharField(choices=[('chinese', 'Chinese'), ('italian', 'Italian'), ('greek', 'Greek')], max_length=15)),
                ('place', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='app_three.place')),
            ],
        ),
    ]
