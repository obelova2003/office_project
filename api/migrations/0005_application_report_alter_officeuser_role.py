# Generated by Django 4.2 on 2024-06-24 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_officeuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('storage_name_from', models.CharField(max_length=250, verbose_name='Хранилище начальное')),
                ('storage_name_to', models.CharField(max_length=250, verbose_name='Хранилище конечное')),
                ('status', models.CharField(choices=[('created', 'создана'), ('work', 'в работе'), ('executed', 'исполнена')], max_length=100, verbose_name='Статус')),
                ('count', models.IntegerField(verbose_name='Кол-во')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_date', models.DateField(auto_now=True, verbose_name='Дата редактирования')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Отчет',
                'verbose_name_plural': 'Отчеты',
            },
        ),
        migrations.AlterField(
            model_name='officeuser',
            name='role',
            field=models.CharField(choices=[('client', 'Клиент'), ('manager', 'Менеджер')], max_length=10),
        ),
    ]
