import django_filters
from django_filters import rest_framework as filters, DateFromToRangeFilter

from advertisements.models import Advertisement


class AdvertisementFilter(django_filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = DateFromToRangeFilter()
    updated_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['status', 'creator', 'created_at', 'updated_at']
