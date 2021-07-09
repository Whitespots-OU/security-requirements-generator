from django.db import models
from django.utils.translation import gettext as _
from django.template.defaultfilters import truncatechars

from solo.models import SingletonModel

__all__ = ["Config", "AssessmentButton", "AdditionalLogo"]


class Config(SingletonModel):
    export_company_name = models.CharField(_("Company name"), max_length=256, default=_("Company name"))

    def __str__(self):
        return _("Config")

    class Meta:
        verbose_name = _("Site config")


class AssessmentButton(SingletonModel):
    button_value = models.CharField(_("Button value"), max_length=256, default=_("Security assessment"))
    button_link = models.CharField(_("Button link"), max_length=256, default=_("https://whitespots.io/security-assessment"))

    def __str__(self):
        return _("Assessment Button")

    class Meta:
        verbose_name = _("Assessment Button")


class AdditionalLogo(models.Model):
    logo = models.ImageField(upload_to='additional_logo')
    enabled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return truncatechars(self.logo, 32)

    class Meta:
        verbose_name = _("Additional logo")