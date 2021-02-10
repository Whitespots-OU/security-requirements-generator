from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.requirement.models import Category, Requirement, ExportRequest

__all__ = ["CreateRequestExportSerializer", "ExportRequestRetrieveSerializer"]


class CreateExportOneCategorySerializer(serializers.Serializer):
    category_id = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())
    requirements_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Requirement.objects.all())


class CreateRequestExportSerializer(serializers.Serializer):
    data = CreateExportOneCategorySerializer(many=True, required=True)
    language = serializers.ChoiceField(
        label=_("Language"),
        choices=[lang[0] for lang in settings.LANGUAGES],
        required=False,
        default=settings.LANGUAGE_CODE,
    )

    def create(self, validated_data) -> ExportRequest:
        data = []
        for cat_data in validated_data["data"]:
            requirements_ids = []
            for requirement in cat_data["requirements_ids"]:
                requirements_ids.append(requirement.pk)
            data.append({"category_id": cat_data["category_id"].id, "requirements_ids": requirements_ids})

        return ExportRequest.objects.create(
            status=ExportRequest.STATUS.CREATED, data=data, language=validated_data["language"]
        )


class ExportRequestRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportRequest
        fields = ["uuid", "status", "file", "created", "finished"]
