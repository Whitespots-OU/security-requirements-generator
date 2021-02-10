from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.views.generic import TemplateView

from apps.common.views import sitemaps

admin.site.site_header = "Whitespots.io"
admin.site.site_title = "Whitespots.io"
admin.site.index_title = "Welcome to Whitespots.io security requirements admin-panel"

urlpatterns = [
    path("api/v1/", include(("apps.api.urls", "apps.api"), namespace="api_v1")),
    path("admin/", admin.site.urls),
    path("admin/martor/", include("martor.urls")),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain", extra_context={"BASE_URL": settings.BASE_URL})),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
