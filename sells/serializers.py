from rest_framework import serializers
from .models import Sell


class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = ['user_id', 'products_id', 'weight', 'created_at']
