# Generated by Django 4.2 on 2024-06-27 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_storage_password_storage_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storage',
            name='column',
            field=models.CharField(max_length=100, unique=True, verbose_name='Столбец'),
        ),
    ]