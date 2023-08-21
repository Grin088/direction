import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


class RefBook(models.Model):
    """Модель справочника"""
    class Meta:
        verbose_name = _('справочник')
        verbose_name_plural = _('справочники')

    code = models.CharField(max_length=100, unique=True, verbose_name=_('код'))
    name = models.CharField(max_length=300, verbose_name=_('наименование'))
    description = models.TextField(blank=True, null=True, verbose_name=_('описание'))

    @property
    def current_version(self):
        """Свойство для вывода текущей версии справочника"""
        today = datetime.date.today()
        version = RefBookVersion.objects.\
            filter(
                ref_book_id=self.id,
                start_date__lte=today)\
            .order_by("start_date").last()
        return version

    def __str__(self):
        return f"id: {self.pk}, код: {self.code}, наименование: {self.name}"


class RefBookVersion(models.Model):
    """Модель версии справочника"""
    class Meta:
        verbose_name = _('версия справочника')
        verbose_name_plural = _('версии справочников')
        unique_together = (('ref_book_id', 'version'), ('ref_book_id', 'start_date'))

    ref_book_id = models.ForeignKey(
        RefBook,
        on_delete=models.CASCADE,
        verbose_name=_('идентификатор справочника')
    )
    version = models.CharField(max_length=50, verbose_name=_('версия'))
    start_date = models.DateField(null=True, blank=True, verbose_name=_('дата начала действия версии'))

    def __str__(self):
        return f"id {self.id},  версия {self.version}, справочник: {self.ref_book_id.name}"


class RefBookElement(models.Model):
    """Модель элемента справочника"""
    class Meta:
        verbose_name = _('элемент справочник')
        verbose_name_plural = _('элементы справочников')
        unique_together = ('ref_book_version_id', 'code')

    ref_book_version_id = models.ForeignKey(
        RefBookVersion,
        on_delete=models.CASCADE,
        verbose_name=_('идентификатор версии справочника')
    )
    code = models.CharField(max_length=100, verbose_name=_('код элемента'))
    value = models.CharField(max_length=300, verbose_name=_('значение элемента'))
