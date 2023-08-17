from rest_framework import generics
from rest_framework.validators import ValidationError
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext_lazy as _
from ref_books.filters import DirectionElementFilter, DirectionsFilter
from ref_books.models import RefBook
from ref_books.services.ref_books_service import get_ref_book_queryset
from ref_books.serializers import DirectionSerializer, DirectionElementSerializer


class DirectionListView(generics.ListAPIView):
    """API view для отображения списка справочников. Если указана дата, возвращаются только те справочники,
     в которых имеются версии с датой начала действия раннее или равной указанной"""

    queryset = RefBook.objects.all()
    serializer_class = DirectionSerializer
    filterset_class = DirectionsFilter


class DirectionElementListView(generics.ListAPIView):
    """API view для отображения списка элементов справочников. Если указана версия справочника то,
     возвращаются элементы указанной версии, иначе элементы текущей версии"""

    serializer_class = DirectionElementSerializer
    filterset_class = DirectionElementFilter

    def get_queryset(self):
        """Пользовательский метод для получения списка значений"""

        ref_book_id = self.kwargs['id']
        ref_book = get_object_or_404(RefBook, id=ref_book_id)
        version = self.request.query_params.get('version', None)
        queryset = get_ref_book_queryset(ref_book_version_id__ref_book_id=ref_book)
        if not version:
            ref_book_version = ref_book.current_version
            queryset = get_ref_book_queryset(ref_book_version_id=ref_book_version)
        return queryset


class CheckElementView(DirectionElementListView):
    """API для валидации элемента справочника - это проверка на то,
    что элемент с данным кодом и значением присутствует в указанной версии справочника."""

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'code',
                openapi.IN_QUERY,
                description='Ref book element code',
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'value',
                openapi.IN_QUERY,
                description='Element value',
                type=openapi.TYPE_STRING,
                required=True
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        """Метод обработки запроса GET"""
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        """Пользовательский метод для получения списка значений"""

        queryset = super().get_queryset()
        code = self.request.query_params.get('code', None)
        value = self.request.query_params.get('value', None)
        if not code or not value:
            raise ValidationError(
                code=400,
                detail=_('Параметры "code" и "value" обязательны'))
        return queryset.filter(code=code, value=value)
