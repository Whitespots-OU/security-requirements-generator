from django.urls import path

from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("category", views.CategoryViewSet, basename="category")
router.register("additional_logo", views.AdditionalLogoViewSet, basename="additional_logo")
router.register("assessment_button", views.AssessmentButtonViewSet, basename="assessment_button")

urlpatterns = [
    path("export/", views.CreateRequestExportView.as_view(), name="request_export-create"),
    path("export/<uuid:pk>/", views.ExportRequestRetrieveDestroyView.as_view(), name="request_export-retrieve"),
    path("requirement/<int:pk>/", views.RequirementRetrieveView.as_view(), name="requirement-retrieve"),
]
urlpatterns += router.urls
