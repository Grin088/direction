from ref_books.models import RefBookElement
from django.db.models.query import QuerySet


def get_ref_book_queryset(**kwargs) -> QuerySet[RefBookElement]:
    """
    Возвращает запрос к базе данных для элементов справочника с заданными фильтрами.
    :param kwargs: Фильтры для запроса
    :return: QuerySet с элементами справочника, удовлетворяющими фильтрам
    """
    queryset = RefBookElement.objects.\
        select_related('ref_book_version_id').\
        filter(**kwargs)
    return queryset
