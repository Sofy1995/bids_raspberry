from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range
from django.contrib.auth.models import User

from django import forms


class CreateBidForm(forms.Form):
    """Form for a librarian to renew books.
    fields = ['text', 'type_bid', 'location', 'telephone_num', 'bider', 'maker', 'helper']"""
    text = forms.CharField(max_length=1000, help_text="Enter a brief description of the bid")

    TYPE_OF_BID = (
        ('h', 'hard'),
        ('c', 'cartridge'),
        ('pr', 'printer'),
        ('w', 'web or net'),
        ('t', 'telephone'),
        ('v', 'viruses'),
        ('s', 'soft'),
        ('pa', 'Parus'),
    )

    boys = User.objects.all()

    type_bid = forms.ChoiceField(choices=TYPE_OF_BID, initial='h')
    location = forms.CharField(initial='', required=False)
    # location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    telephone_num = forms.CharField(initial='', required=False)
    # telephone_num = models.ForeignKey('Telephone', on_delete=models.SET_NULL, null=True)
    bider = forms.CharField(initial='', required=False)
    # bider = models.ForeignKey('Bider', on_delete=models.SET_NULL, null=True)
    maker = forms.ModelChoiceField(boys, required=False)
    helper = forms.ModelChoiceField(boys, required=False)
    # helper = models.ManyToManyField('Helper')
    # time_creation = forms.DateTimeField()
    # time_start = forms.DateTimeField()
    # time_done = forms.DateTimeField()

    STATUS = (
        ('a', 'принята'),
        ('w', 'в работе'),
        ('f', 'выполнена'),
    )

    status = forms.ChoiceField(choices=STATUS, initial='a')
    comment = forms.CharField(initial='', required=False)
    result = forms.CharField(initial='', required=False)

    def clean_location(self):
        data = self.cleaned_data['location']
        if data == "":
            raise ValidationError(_('Invalid location - type correct location'))
        # Check date is in range librarian allowed to change (+4 weeks)
        # if data > datetime.date.today() + datetime.timedelta(weeks=4):
        #     raise ValidationError(
        #         _('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

    def clean_telephone_num(self):
        data = self.cleaned_data['telephone_num']
        if data == "":
            raise ValidationError(_('Invalid telephone_num - type correct telephone_num'))
        return data


    def clean(self):
        cleaned_data = super(CreateBidForm, self).clean()
        status = cleaned_data.get("status")
        result = cleaned_data.get("result")

        if status == 'f' and result == '':
            raise ValidationError(_('Invalid result for the status - type any result'))



class CreateStickerForm(forms.Form):
    """Form for a librarian to renew books.
    fields = ['text', 'type_bid', 'location', 'telephone_num', 'bider', 'maker', 'helper']"""
    text = forms.CharField(initial='', required=False)

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == "":
            raise ValidationError(_('Type something'))
        return data
