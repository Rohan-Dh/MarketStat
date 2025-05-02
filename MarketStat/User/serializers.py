from rest_framework import serializers
from .models import *

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class CollectionUserCollectionSerializer(serializers.ModelSerializer):
    collectionId = CollectionSerializer(source="collectionId", many=True)
    class Meta:
        model = UserCollection
        fields = '__all__'