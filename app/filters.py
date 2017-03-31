from app.models import Symbol, SymbolHistory
import django_filters
from django.db.models import Q


# http://django-filter.readthedocs.io/en/develop/guide/rest_framework.html

class SymbolFilter(django_filters.FilterSet):
    symbol = django_filters.CharFilter(lookup_expr='icontains')
    company = django_filters.CharFilter(lookup_expr='icontains')
    sector = django_filters.CharFilter(lookup_expr='icontains')
    industry = django_filters.CharFilter(lookup_expr='icontains')

    symbol_or_company = django_filters.CharFilter(method='filter_symbol_or_company')

    min_growth_rate = django_filters.NumberFilter(name="growth_rate", lookup_expr='gte')
    max_growth_rate = django_filters.NumberFilter(name="growth_rate", lookup_expr='lte')

    min_market_cap = django_filters.NumberFilter(name="market_cap", lookup_expr='gte')
    max_market_cap = django_filters.NumberFilter(name="market_cap", lookup_expr='lte')

    class Meta:
        model = Symbol
        fields = ['min_growth_rate', 'max_growth_rate',
                  'min_market_cap', 'max_market_cap',
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
