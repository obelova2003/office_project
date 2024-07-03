from django.db import models

from django.contrib.auth.models import AbstractUser 
from .validators import validate_host
from django.core.validators import MinValueValidator, MaxValueValidator

ROLES = (
    ('client', 'Клиент'),
    ('manager', 'Менеджер'),
    ('director', 'Директор')
)

STATUS = (
    ('created', 'создана'),
    ('work', 'в работе'),
    ('executed', 'исполнена'),
)
class OfficeUser(AbstractUser):
    username = models.CharField(max_length=150,
                                unique=True,
                                verbose_name='Логин')
    first_name= models.CharField(max_length=150,
                                 verbose_name='Имя')
    last_name = models.CharField(max_length=150,
                                 verbose_name='Фамилия')
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name='Почта')
    role = models.CharField(max_length=10, choices=ROLES)
    manager = models.ForeignKey("OfficeUser",
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_manager(self):
        return self.role == 'manager'

    @property
    def is_client(self):
        return self.role == 'client'
    
    @property
    def is_director(self):
        return self.role == 'director'

    def __str__(self):
        return self.username
    

class Report(models.Model):
    number = models.IntegerField(verbose_name='Номер')
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'

    def __str__(self):
        return f'Отчет № {self.number}'


class Application(models.Model):
    number = models.IntegerField(verbose_name='Номер')
    author_client = models.ForeignKey("OfficeUser",
                                        on_delete=models.CASCADE,
                                        null=True,
                                        blank=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    storage_name_from  = models.CharField(max_length=100, verbose_name='Имя хранилища начального')
    storage_name_to = models.CharField(max_length=100, verbose_name='Имя хранилища конечного')
    status = models.CharField(max_length=100, choices=STATUS, verbose_name='Статус')
    count = models.IntegerField(verbose_name='Кол-во')
    create_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    update_date = models.DateField(auto_now=True, verbose_name='Дата редактирования')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'Заявка № {self.number}'


class Storage(models.Model):
    host = models.CharField(validators=(validate_host,),
                            max_length=100, verbose_name= 'Хост')
    port = models.IntegerField(validators=[MinValueValidator(1),
                                           MaxValueValidator(999999)],
                               verbose_name='Порт')
    user = models.CharField(max_length=100, default='user', verbose_name= 'Логин')
    password = models.CharField(max_length=100, default='password', verbose_name= 'Пароль')
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    table = models.CharField(max_length=100, unique=True, verbose_name='Таблица')
    column = models.CharField(max_length=100, unique=True, verbose_name='Столбец')

    class Meta:
        verbose_name = 'Хранилище'
        verbose_name_plural = 'Хранилища'

    def __str__(self):
        return self.name