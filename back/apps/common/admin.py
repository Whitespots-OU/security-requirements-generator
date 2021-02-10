from django.contrib import admin
from django.utils.translation import gettext as _

from solo.admin import SingletonModelAdmin

from .models import Config


@admin.register(Config)
class ConfigAdmin(SingletonModelAdmin):
    fieldsets = ((_("Export to PDF"), {"fields": ("export_company_name",)}),)
