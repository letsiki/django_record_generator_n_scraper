# Generated by Django 5.0.11 on 2025-03-21 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_three', '0007_b'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='b',
            options={'verbose_name_plural': 'plural'},
        ),
        migrations.AddField(
            model_name='b',
            name='name2',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
