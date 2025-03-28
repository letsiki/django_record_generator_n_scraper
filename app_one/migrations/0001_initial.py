# Generated by Django 5.0.11 on 2025-03-18 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('age', models.SmallIntegerField()),
                ('description', models.TextField(max_length=200)),
                ('has_kids', models.BooleanField(default=False, verbose_name='do you have kids?')),
                ('is_married', models.BooleanField(default=False, verbose_name='are you married?')),
                ('dob', models.DateField(verbose_name='date of birth')),
                ('id_number', models.IntegerField(unique=True)),
                ('favorite_player', models.CharField(choices=[('cristiano', 'Cristiano Ronaldo'), ('messi', 'Lionel Messi')], max_length=30)),
                ('favorite_sport', models.CharField(choices=[('tennis', 'Tennis'), ('soccer', 'Soccer'), ('basketball', 'Basketball')], max_length=30)),
            ],
        ),
    ]
