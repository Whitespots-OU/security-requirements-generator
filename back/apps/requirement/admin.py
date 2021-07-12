from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from modeltranslation.admin import TranslationAdmin
from adminsortable2.admin import SortableAdminMixin
from django.db import models
from django.utils.translation import gettext as _

from martor.widgets import AdminMartorWidget

from .models import Requirement, Category, TestCase, ExportRequest


class MarkDownMixin:
    formfield_overrides = {models.TextField: {"widget": AdminMartorWidget}}


class TranslationMedia:
    js = (
        "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js",
        "modeltranslation/js/force_jquery.js",
        "modeltranslation/js/tabbed_translation_fields.js",
    )
    css = {"screen": ("modeltranslation/css/tabbed_translation_fields.css",)}


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, TranslationAdmin, admin.ModelAdmin):
    list_display = ["name_en", "show_at_home", "is_default"]
    search_fields = ["name"]
    list_filter = ["show_at_home"]
    list_editable = ["show_at_home", "is_default"]

    class Media(TranslationMedia):
        ...


@admin.register(Requirement)
class RequirementAdmin(MarkDownMixin, TranslationAdmin, admin.ModelAdmin):
    filter_horizontal = ["test_cases", "categories"]

    list_display = ["title_en", "categories_flat_list", "is_default"]
    search_fields = ["title"]
    list_editable = ['is_default']
    fieldsets = (
        (_("Description"), {'fields': ("title", "summary", "text", )}),
        (_("Categories"), {'fields': ("categories", )}),
        (_("Test cases"), {'fields': ("test_cases", )}),
    )

    def categories_flat_list(self, obj: Requirement) -> str:
        return ", ".join(obj.categories.values_list("name", flat=True)) + f" (total: {obj.categories.count()})"

    categories_flat_list.short_description = "Categories"

    class Media(TranslationMedia):
        ...


@admin.register(TestCase)
class TestCaseAdmin(MarkDownMixin, TranslationAdmin, admin.ModelAdmin):
    list_display = ["title_en"]
    search_fields = ["title"]

    class Media(TranslationMedia):
        ...


@admin.register(ExportRequest)
class ExportRequestAdmin(admin.ModelAdmin):
    formfield_overrides = {JSONField: {"widget": JSONEditorWidget}}
    radio_fields = {"language": admin.HORIZONTAL, "status": admin.HORIZONTAL}

    list_display = ["uuid", "status", "created", "finished"]
    list_filter = ["status", "created", "finished"]
