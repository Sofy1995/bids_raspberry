# Generated by Django 3.1.5 on 2021-06-18 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='status',
            field=models.CharField(choices=[('a', 'Принята'), ('w', 'В работе'), ('f', 'Выполнена')], default='a', max_length=1, verbose_name='Статус заявки'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='type_bid',
            field=models.CharField(blank=True, choices=[('h', 'Железо'), ('c', 'Картридж'), ('pr', 'Принтер'), ('w', 'Сеть'), ('t', 'Телефон'), ('v', 'Вирусы'), ('s', 'Софт'), ('pa', 'Парус')], default='h', max_length=2, verbose_name='Тип заявки'),
        ),
    ]