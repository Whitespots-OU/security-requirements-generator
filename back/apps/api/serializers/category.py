from rest_framework import serializers

from apps.requirement.models import Category, Requirement, TestCase

__all__ = ["CategorySerializer"]


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ["id", "title", "text"]


class RequirementSerializer(serializers.ModelSerializer):
    test_cases = TestCaseSerializer(many=True)

    class Meta:
        model = Requirement
        fields = ["id", "title", "summary", "text", "test_cases"]


class CategorySerializer(serializers.ModelSerializer):
    requirements = RequirementSerializer(many=True, source="requirement_set.all")

    class Meta:
        model = Category
        fields = ["id", "name", "summary", "requirements"]
