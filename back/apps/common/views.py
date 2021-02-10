from django.contrib.sitemaps import Sitemap
from django.conf import settings

from apps.requirement.models import Requirement


__all__ = ["sitemaps"]


class StaticViewSitemap(Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        results = []
        for language in settings.LANGUAGES:
            for url in ["/", "/export"]:
                results.append((language[0], url))

        return results

    def location(self, item):
        return f"/{item[0]}/{item[1]}"


class RequirementViewSitemap(Sitemap):
    priority = 1
    changefreq = "weekly"

    def items(self):
        results = []
        for language in settings.LANGUAGES:
            for req_id in Requirement.objects.values_list("id", flat=True):
                results.append((language[0], req_id))

        return results

    def location(self, item: list) -> str:
        return f"/{item[0]}/requirement/{item[1]}"


sitemaps = {"static": StaticViewSitemap(), "requirement": RequirementViewSitemap()}
