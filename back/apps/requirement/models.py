from uuid import uuid4

from django.conf import settings
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.utils.translation import gettext as _

__all__ = ["Category", "Requirement", "TestCase", "ExportRequest"]


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=128)
    summary = models.TextField(_("Summary"), max_length=1024, help_text=_("Hint at left panel"))
    show_at_home = models.BooleanField(_("Show at home"), default=True)
    is_default = models.BooleanField(_("Default category"), default=False)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self) -> str:
        return truncatechars(self.name_en, 32)

    class Meta:
        ordering = ["order"]
        app_label = "requirement"
        verbose_name = "category"
        verbose_name_plural = "Categories"


class Requirement(models.Model):
    categories = models.ManyToManyField("Category", verbose_name=_("Categories"))
    title = models.CharField(_("Title"), max_length=128)
    summary = models.TextField(_("Summary"), max_length=1024)
    text = models.TextField(_("Text"))
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    is_default = models.BooleanField(_("Default requirement"), default=False)
    test_cases = models.ManyToManyField("TestCase", blank=True, verbose_name=_("Test cases"))

    def __str__(self) -> str:
        return truncatechars(self.title_en, 32)

    class Meta:
        ordering = ["order"]
        app_label = "requirement"


class TestCase(models.Model):
    title = models.CharField(_("Title"), max_length=128)
    text = models.TextField(_("Text"))

    def __str__(self) -> str:
        return truncatechars(self.title_en, 32)

    class Meta:
        app_label = "requirement"


class ExportRequest(models.Model):
    class STATUS(models.TextChoices):
        CREATED = "created", _("Created")
        STARTED = "started", _("Started")
        FINISHED = "finished", _("Finished")
        FAILED = "failed", _("Failed")

    uuid = models.UUIDField(_("Unique ID"), default=uuid4, help_text=_("For downloading"), primary_key=True)
    status = models.CharField(_("Status"), max_length=32, default=STATUS.CREATED, choices=STATUS.choices)
    file = models.FileField(_("File"), upload_to="exports", blank=True, null=True)
    data = models.JSONField(_("Export data"))
    language = models.CharField(_("Language"), max_length=6, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)

    created = models.DateTimeField(_("Created"), default=timezone.now)
    finished = models.DateTimeField(_("Finished"), blank=True, null=True)

    def __stt__(self) -> str:
        return str(self.uuid)

    class Meta:
        ordering = ["created"]
        app_label = "requirement"
