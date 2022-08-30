from rest_framework import serializers

from .models import Category, Product, Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('image',)


class ProductSerializer(serializers.ModelSerializer):
    photo = PhotoSerializer(many=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='slug')

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'url',
            'description',
            'price',
            'available',
            'photo',
        )


class CategorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'product')
