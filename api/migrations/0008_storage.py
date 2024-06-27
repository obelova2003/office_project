# Generated by Django 4.2 on 2024-06-27 08:40

import api.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_officeuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=100, validators=[api.validators.validate_host], verbose_name='Хост')),
                ('port', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999999)], verbose_name='Порт')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('table', models.CharField(max_length=100, unique=True, verbose_name='Таблица')),
                ('column', models.CharField(max_length=100, unique=True, verbose_name='Колонна')),
            ],
            options={
                'verbose_name': 'Хранилище',
                'verbose_name_plural': 'Хранилища',
            },
        ),
    ]
