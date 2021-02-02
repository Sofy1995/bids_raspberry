from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range
from django.contrib.auth.models import User

from django import forms


class CreateBidForm(forms.Form):
    """Form for a librarian to renew books.
    fields = ['text', 'type_bid', 'location', 'telephone_num', 'bider', 'maker', 'helper']"""
    text = forms.CharField(max_length=1000, widget=forms.Textarea, label='Содержание')

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

    boys = User.objects.all()

    type_bid = forms.ChoiceField(choices=TYPE_OF_BID, initial='h', label='Тип заявки')
    location = forms.CharField(initial='', required=False, label='Место')
    # location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    telephone_num = forms.CharField(initial='', required=False, label='Телефон')
    # telephone_num = models.ForeignKey('Telephone', on_delete=models.SET_NULL, null=True)
    bider = forms.CharField(initial='', required=False, label='Заявитель')
    # bider = models.ForeignKey('Bider', on_delete=models.SET_NULL, null=True)
    maker = forms.ModelChoiceField(boys, required=False, label='Исполнитель')
    helper = forms.ModelChoiceField(boys, required=False, label='Ассистент')
    # helper = models.ManyToManyField('Helper')
    # time_creation = forms.DateTimeField()
    # time_start = forms.DateTimeField()
    # time_done = forms.DateTimeField()

    STATUS = (
        ('a', 'принята'),
        ('w', 'в работе'),
        ('f', 'выполнена'),
    )

    status = forms.ChoiceField(choices=STATUS, initial='a', label='Состояние')
    comment = forms.CharField(initial='', required=False, label='Комментарий')
    result = forms.CharField(initial='', required=False, label='Результат')

    def clean_location(self):
        data = self.cleaned_data['location']
        if data == "":
            raise ValidationError(_('Вы не указали место, в котором локализована проблема'))
        # Check date is in range librarian allowed to change (+4 weeks)
        # if data > datetime.date.today() + datetime.timedelta(weeks=4):
        #     raise ValidationError(
        #         _('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

    def clean_telephone_num(self):
        data = self.cleaned_data['telephone_num']
        if data == "":
            raise ValidationError(_('Вы не указали номер телефона для связи с заявителем'))
        return data


    def clean(self):
        cleaned_data = super(CreateBidForm, self).clean()
        status = cleaned_data.get("status")
        result = cleaned_data.get("result")

        if status == 'f' and result == '':
            raise ValidationError(_('Для завершения работы по заявке укажите результат работы'))



class CreateStickerForm(forms.Form):
    """Form for a librarian to renew books.
    fields = ['text', 'type_bid', 'location', 'telephone_num', 'bider', 'maker', 'helper']"""
    text = forms.CharField(initial='', required=False, widget=forms.Textarea, label='Содержание')

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == "":
            raise ValidationError(_('Напишите хоть что-нибудь'))
        return data


class SearchForm(forms.Form):
    query = forms.IntegerField(label='Введите номер заявки')
    # query = forms.CharField()
