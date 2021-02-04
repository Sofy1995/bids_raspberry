from django.db import models
import uuid
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Bid(models.Model):

    text = models.TextField(max_length=1000, help_text="Enter a brief description of the bid", verbose_name="Текст заявки")

    TYPE_OF_BID = (
        ('h', 'железо'),
        ('c', 'картридж'),
        ('pr', 'принтер'),
        ('w', 'сеть'),
        ('t', 'телефон'),
        ('v', 'вирусы'),
        ('s', 'софт'),
        ('pa', 'Парус'),
    )

    type_bid = models.CharField(max_length=2, choices=TYPE_OF_BID, blank=True, default='h', verbose_name="Тип заявки")
    location = models.CharField(max_length=200, default='Кабинет', verbose_name="Кабинет")
    # location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    telephone_num = models.CharField(max_length=200, default='Телефон', verbose_name="Телефон")
    # telephone_num = models.ForeignKey('Telephone', on_delete=models.SET_NULL, null=True)
    bider = models.CharField(max_length=200, default='', verbose_name="Заявитель")
    # bider = models.ForeignKey('Bider', on_delete=models.SET_NULL, null=True)
    maker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Исполнитель")
    helper = models.CharField(max_length=200, null=True, verbose_name="Помощник")
    # helper = models.ManyToManyField('Helper')
    time_creation = models.DateTimeField(null=True, verbose_name="Дата создания заявки")
    time_start = models.DateTimeField(null=True, verbose_name="Дата начала работы")
    time_done = models.DateTimeField(null=True, verbose_name="Дата завершения работы")

    STATUS = (
        ('a', 'принята'),
        ('w', 'в работе'),
        ('f', 'выполнена'),
    )

    status = models.CharField(max_length=1, choices=STATUS, default='a', verbose_name="Статус заявки")
    comment = models.CharField(max_length=200, default='', verbose_name="Комментарий")
    result = models.CharField(max_length=300, default='', verbose_name="Результат работы")

    class Meta:
      #   ordering = ["time_creation"]
        verbose_name_plural = "Заявки"
        verbose_name = "Заявка"

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('bid-detail', args=[str(self.id)])


class Sticker(models.Model):
    text = models.CharField(max_length=200, verbose_name="Текст объявления")
    date_creation = models.DateTimeField(null=True, verbose_name="Дата создания")
    STATUS = (
        ('v', 'visible'),
        ('h', 'hidden'),
            )

    status = models.CharField(max_length=1, choices=STATUS, default='v', verbose_name="Статус")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "Объявления"
        verbose_name = "Объявление"


