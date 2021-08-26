import django_filters
from django_filters import rest_framework as filters

from .models import Bid


class BidFilter(filters.FilterSet):
    time_done = filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(
        attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = Bid
        fields = ['maker', "time_done"]

