from django.contrib import admin
from django.utils.translation import gettext as _

from solo.admin import SingletonModelAdmin

from .models import Config, AssessmentButton


@admin.register(Config)
class ConfigAdmin(SingletonModelAdmin):
    fieldsets = ((_("Export to PDF"), {"fields": ("export_company_name",)}),)


@admin.register(AssessmentButton)
class AssessmentButtonAdmin(SingletonModelAdmin):
    fieldsets = (
        (_("Assessment Button Value"), {'fields': ("button_value", )}),
        (_("Assessment Button Link"), {'fields': ("button_link", )}),
    )