from app.models import Symbol, SymbolHistory
import django_filters
from django.db.models import Q


def generate_number_filters(field):
    min_ = django_filters.NumberFilter(name=field, lookup_expr='gte')
    max_ = django_filters.NumberFilter(name=field, lookup_expr='lte')
    return min_, max_

# http://django-filter.readthedocs.io/en/develop/guide/rest_framework.html

class SymbolFilter(django_filters.FilterSet):
    symbol = django_filters.CharFilter(lookup_expr='icontains')
    company = django_filters.CharFilter(lookup_expr='icontains')
    sector = django_filters.CharFilter(lookup_expr='icontains')
    industry = django_filters.CharFilter(lookup_expr='icontains')

    symbol_or_company = django_filters.CharFilter(method='filter_symbol_or_company')

    min_growth_rate, max_growth_rate = generate_number_filters('growth_rate')
    min_moving_average, max_moving_average = generate_number_filters('moving_average')
    min_market_cap, max_market_cap = generate_number_filters('market_cap')
    min_last_close, max_last_close = generate_number_filters('last_close')
    min_average_volume, max_average_volume = generate_number_filters('average_volume')


    class Meta:
        model = Symbol
        fields = ['min_growth_rate', 'max_growth_rate',
                  'min_market_cap', 'max_market_cap',
                  'min_moving_average', 'max_moving_average',
                  'min_average_volume', 'max_average_volume',
                  'min_last_close', 'max_last_close',
                  'symbol',
                  'company',
                  'sector',
                  'industry',
                  'symbol_or_company'
                  ]

    def filter_symbol_or_company(self, queryset, name, value):
        return queryset.filter(Q(symbol__contains=value) | Q(company__contains=value))


class SymbolHistoryFilter(django_filters.FilterSet):
    min_open = django_filters.NumberFilter(name="open", lookup_expr='gte')
    max_open = django_filters.NumberFilter(name="open", lookup_expr='lte')

    min_high = django_filters.NumberFilter(name="high", lookup_expr='gte')
    max_high = django_filters.NumberFilter(name="high", lookup_expr='lte')

    min_low = django_filters.NumberFilter(name="low", lookup_expr='gte')
    max_low = django_filters.NumberFilter(name="low", lookup_expr='lte')

    min_volume = django_filters.NumberFilter(name="volume", lookup_expr='gte')
    max_volume = django_filters.NumberFilter(name="volume", lookup_expr='lte')

    min_close = django_filters.NumberFilter(name="close", lookup_expr='gte')
    max_close = django_filters.NumberFilter(name="close", lookup_expr='lte')

    class Meta:
        model = SymbolHistory
        fields = ['min_open', 'max_open', 'min_low', 'max_low', 'min_volume', 'max_volume',
                  'min_close', 'max_close']
