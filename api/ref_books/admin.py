from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import RefBook, RefBookVersion, RefBookElement


class DirectionVersionsInline(admin.TabularInline):
    """
    Встроенная форма для отображения версий справочника в административной панели.
    """
    model = RefBookVersion
    extra = 1


class DirectionElementsInline(admin.TabularInline):
    """
    Встроенная форма для отображения элементов справочника в административной панели.
    """
    model = RefBookElement
    extra = 1


@admin.register(RefBook)
class DirectionAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели Direction.
    """
    inlines = [DirectionVersionsInline]
    list_display = ('id', 'code', 'name', 'latest_version', 'issue_date')

    def latest_version(self, obj):
        """
        Возвращает номер последней версии справочника.
        """
        try:
            return obj.current_version.version
        except AttributeError:
            return None

    def issue_date(self, obj):
        """
        Возвращает дату начала действия текущей версии справочника.
        """
        try:
            return obj.current_version.start_date
        except AttributeError:
            return None

    latest_version.short_description = _('текущая версия')
    issue_date.short_description = _('дата начала действия версии')


@admin.register(RefBookVersion)
class DirectionVersionAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели DirectionVersion.
    """
    inlines = [DirectionElementsInline]
    list_display = ('ref_book_name', 'ref_book_code', 'version', 'start_date')

    def ref_book_name(self, obj):
        """
        Возвращает наименование связанного справочника.
        """
        return obj.ref_book_id.name

    def ref_book_code(self, obj):
        """
        Возвращает код связанного справочника.
        """
        return obj.ref_book_id.code

    ref_book_name.short_description = _('наименование справочника')
    ref_book_name.short_description = _('код справочника')


@admin.register(RefBookElement)
class DirectionElementAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели DirectionElement.
    """
    list_display = ('id', 'ref_book_version_id', 'code', 'value')
