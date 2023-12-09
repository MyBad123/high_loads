from rest_framework import serializers


class AddProductSerializer(serializers.Serializer):
    products = serializers.ListField(child=serializers.IntegerField())
