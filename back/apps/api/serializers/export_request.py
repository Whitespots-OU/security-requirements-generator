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
        default_data = []
        default_categories = Category.objects.filter(is_default=True).all()
        for category in default_categories:
            reqs = Requirement.objects.filter(is_default=True).filter(categories__in=[category]).all()
            requirements_ids = []
            for requirement in reqs:
                requirements_ids.append(requirement.pk)
            default_data.append({"category_id": category.id, "requirements_ids": requirements_ids})

        actual_data = []
        for cat_data in validated_data["data"]:
            requirements_ids = []
            for requirement in cat_data["requirements_ids"]:
                requirements_ids.append(requirement.pk)
            actual_data.append({"category_id": cat_data["category_id"].id, "requirements_ids": requirements_ids})

        if default_data:
            for actual_req in actual_data:
                for default_req in default_data:
                    if default_req["category_id"] == actual_req["category_id"]:
                        actual_req["requirements_ids"] = list(set(actual_req["requirements_ids"] + 
                                                                  default_req["requirements_ids"]))

            for default_req in reversed(default_data):
                count = 0
                for actual_req in actual_data:
                    if default_req["category_id"] == actual_req["category_id"]:
                        count += 1
                if count == 0:
                    actual_data.insert(0, default_req)

        return ExportRequest.objects.create(
            status=ExportRequest.STATUS.CREATED, data=actual_data, language=validated_data["language"]
        )


class ExportRequestRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportRequest
        fields = ["uuid", "status", "file", "created", "finished"]
