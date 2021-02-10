from django.db import models
from django.utils.translation import gettext as _

from solo.models import SingletonModel

__all__ = ["Config"]


class Config(SingletonModel):
    export_company_name = models.CharField(_("Company name"), max_length=256, default=_("Company name"))

    def __str__(self):
        return _("Config")

    class Meta:
        verbose_name = _("Site config")
