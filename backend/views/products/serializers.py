from rest_framework import serializers
from backend.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """serializer for Product from db"""

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """serializer for Product from db"""

    class Meta:
        model = Product
        fields = '__all__'


class ProductWithCategorySerializer(serializers.Serializer):
    category = CategorySerializer()
    product = ProductSerializer()


class QueryProductSerializer(serializers.Serializer):
    min = serializers.BooleanField(allow_null=True)
    max = serializers.BooleanField(allow_null=True)
    sort = serializers.CharField(allow_null=True)


class QuerySerializer(serializers.Serializer):
    pk = serializers.IntegerField()



