from rest_framework import serializers

from store.models import Product


class ProductListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
