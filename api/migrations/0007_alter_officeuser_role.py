# Generated by Django 4.2 on 2024-06-26 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_application_author_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officeuser',
            name='role',
            field=models.CharField(choices=[('client', 'Клиент'), ('manager', 'Менеджер'), ('director', 'Директор')], max_length=10),
        ),
    ]