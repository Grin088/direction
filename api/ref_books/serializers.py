from rest_framework import serializers
from ref_books.models import RefBook, RefBookElement


class DirectionElementSerializer(serializers.ModelSerializer):
    """Сериализатор модели элемента справочника"""

    class Meta:
        model = RefBookElement
        fields = ('code', 'value')


class DirectionSerializer(serializers.ModelSerializer):
    """Сериализатор модели справочника"""
    class Meta:
        model = RefBook
        fields = ('id', 'code', 'name')
