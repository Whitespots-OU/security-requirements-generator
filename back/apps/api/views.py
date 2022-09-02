import os

from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response

from apps.common.models import AdditionalLogo, AssessmentButton
from apps.requirement import models
from apps.requirement.tasks import generate_pdf

from . import serializers

__all__ = ["CategoryViewSet", "CreateRequestExportView", "ExportRequestRetrieveDestroyView", "ProductViewSet"]


class ProductViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.Product.objects.all().order_by("-id")
    serializer_class = serializers.ProductSerializer
      
    def partial_update(self, request, pk=None):
        product = self.get_object()
        serializer = serializers.ProductSerializer(product, partial=True)
        if 'categories' not in request.data:
            raise ValidationError("You need to add categories")

        product = models.Product.objects.get(id=pk)
        product.categories.set(request.data["categories"])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Category.objects.filter(show_at_home=True).all()
    serializer_class = serializers.CategorySerializer


class RequirementRetrieveView(RetrieveAPIView):
    queryset = models.Requirement.objects.all()
    serializer_class = serializers.RequirementSerializer


class CreateRequestExportView(CreateAPIView):
    serializer_class = serializers.CreateRequestExportSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        export_request: models.ExportRequest = self.perform_create(serializer)

        serializer = serializers.ExportRequestRetrieveSerializer(instance=export_request)
        headers = self.get_success_headers(serializer.data)
        serializer = serializers.ExportRequestRetrieveSerializer(export_request)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer: serializers.CreateRequestExportSerializer) -> models.ExportRequest:
        obj: models.ExportRequest = serializer.save()

        transaction.on_commit(lambda: generate_pdf.send(str(obj.uuid)))

        return obj


class ExportRequestRetrieveDestroyView(RetrieveDestroyAPIView):
    queryset = models.ExportRequest.objects.all()
    serializer_class = serializers.ExportRequestRetrieveSerializer

    def perform_destroy(self, instance: models.ExportRequest):
        os.unlink(instance.file.path)
        instance.delete()


class AssessmentButtonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AssessmentButton.objects.all()
    serializer_class = serializers.AssessmentButtonSerializer


class AdditionalLogoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdditionalLogo.objects.filter(enabled=True).all()
    serializer_class = serializers.AdditionalLogoSerializer
