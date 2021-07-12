from rest_framework import serializers

from apps.common.models import AdditionalLogo

__all__ = ["AdditionalLogoSerializer"]


class AdditionalLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalLogo
        fields = ["logo"]