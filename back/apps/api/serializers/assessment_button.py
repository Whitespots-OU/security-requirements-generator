from rest_framework import serializers

from apps.common.models import AssessmentButton

__all__ = ["AssessmentButtonSerializer"]


class AssessmentButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentButton
        fields = ["button_value", "button_link"]