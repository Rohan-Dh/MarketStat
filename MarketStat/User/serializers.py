from rest_framework import serializers
from .models import *

from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format="%d %b %Y, %I:%M %p")
    date_joined = serializers.DateTimeField(format="%d %b %Y, %I:%M %p")
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined', 'last_login']

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class CollectionUserCollectionSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer(source = "collectionId")
    user = UserSerializer(source = "userId")
    created_at = serializers.DateTimeField(format="%d %b %Y, %I:%M %p")
    updated_at = serializers.DateTimeField(format="%d %b %Y, %I:%M %p")
    class Meta:
        model = UserCollection
        fields = ["userCollectionId", "collection", "quantity", "initialPrice", "created_at", "updated_at", "user"]
    

class TransactionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %b %Y, %I:%M %p")
    updated_at = serializers.DateTimeField(format="%d %b %Y, %I:%M %p")
    collection = CollectionUserCollectionSerializer(source = "user_collection")
    class Meta:
        model = Transaction
        fields = ["transactionId", "quantitySold", "soldPrice", "profit", "loss", "soldTo", "created_at", "updated_at", "collection"]