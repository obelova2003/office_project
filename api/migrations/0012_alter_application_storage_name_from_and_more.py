# Generated by Django 4.2 on 2024-07-01 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_application_storage_name_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='storage_name_from',
            field=models.CharField(max_length=100, verbose_name='Имя хранилища начального'),
        ),
        migrations.AlterField(
            model_name='application',
            name='storage_name_to',
            field=models.CharField(max_length=100, verbose_name='Имя хранилища конечного'),
        ),
    ]