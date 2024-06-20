from django.db import models

from django.contrib.auth.models import AbstractUser 

ROLES = (
    ('manager', 'Менеджер'),
    ('client', 'Клиент')
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
    role = models.CharField(max_length=10, choices=ROLES, default='client')
    manager = models.ForeignKey("OfficeUser",
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username