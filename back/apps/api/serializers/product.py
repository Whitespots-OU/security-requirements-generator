from rest_framework import serializers

from apps.requirement.models import Product
from .category import CategorySerializer

__all__ = ["ProductSerializer"]


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ["id", "name", "categories"]
