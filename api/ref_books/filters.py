import django_filters
from ref_books.models import RefBook, RefBookElement


class DirectionsFilter(django_filters.FilterSet):
    """
    Фильтры для списка справочников.

    :param date: Фильтр по дате начала действия версии справочника (меньше или равно)
    """
    date = django_filters.DateFilter(field_name='refbookversion__start_date', lookup_expr='lte')

    class Meta:
        model = RefBook
        fields = ['date']

    def filter_queryset(self, queryset):
        """Пользовательский метод для возврата уникальных значений"""
        queryset = super().filter_queryset(queryset)
        return queryset.distinct()


class DirectionElementFilter(django_filters.FilterSet):
    """
    Фильтры для списка элементов справочника.

    :param version: Фильтр по версии справочника
    """
    version = django_filters.CharFilter(field_name='ref_book_version_id__version', lookup_expr='exact')

    class Meta:
        model = RefBookElement
        fields = ['version']
