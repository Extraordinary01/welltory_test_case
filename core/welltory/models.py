from django.contrib.auth.models import User
from django.db import models


class DataType(models.Model):
    name = models.CharField(verbose_name='Название', max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип данных'
        verbose_name_plural = 'Типы данных'


class Correlation(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    x_data_type = models.ForeignKey(DataType, verbose_name='Тип данных X', on_delete=models.CASCADE,
                                    related_name='x_data_type')
    y_data_type = models.ForeignKey(DataType, verbose_name='Тип данных Y', on_delete=models.CASCADE,
                                    related_name='y_data_type')
    value = models.DecimalField(verbose_name='Коэффициент корреляции', max_digits=5, decimal_places=3)
    p_value = models.DecimalField(verbose_name='Проверка наличия корреляции', max_digits=5, decimal_places=3)

    def __str__(self):
        return f'{self.user} - {self.x_data_type} - {self.y_data_type}'

    class Meta:
        unique_together = ("user", "x_data_type", "y_data_type")
        verbose_name = 'Корреляция'
        verbose_name_plural = 'Корреляции'
