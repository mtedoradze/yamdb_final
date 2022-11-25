import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )
    year = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='exact'
    )
    genre = django_filters.CharFilter(
        field_name='genre',
        lookup_expr='slug',
    )
    category = django_filters.CharFilter(
        field_name='category',
        lookup_expr='slug',
    )

    class Meta:
        model = Title
        fields = ['name', 'year', 'category', 'genre']
