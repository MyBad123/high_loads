from rest_framework import serializers
from backend.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """serializer for Product from db"""

    class Meta:
        model = Product
        fields = ['name', 'about', 'price']


class QueryProductSerializer(serializers.Serializer):
    min = serializers.BooleanField(allow_null=True)
    max = serializers.BooleanField(allow_null=True)
    sort = serializers.CharField()
