import django_filters
from django_filters import rest_framework as filters

from .models import Bid


class BidListFilter(filters.FilterSet):

    class Meta:
        model = Bid
        fields = ['maker']


class BidArchiveFilter(filters.FilterSet):
    time_done = filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(
        attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = Bid
        fields = ['maker', 'time_done']


class BidUserFilter(filters.FilterSet):

    class Meta:
        model = Bid
        fields = ['type_bid']