from rest_framework import serializers

from apps.requirement.models import Category, Requirement, TestCase

__all__ = ["RequirementSerializer"]


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ["id", "title", "text"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "summary"]


class RequirementSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    test_cases = TestCaseSerializer(many=True)

    class Meta:
        model = Requirement
        fields = ["id", "title", "summary", "text", "categories", "test_cases"]
