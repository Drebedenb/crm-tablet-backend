from rest_framework import serializers
from .models import WorkersMain, OrdersMain, WorkersUserAccess


class WorkersSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = WorkersMain


class WorkersUserAccessSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = WorkersUserAccess


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = OrdersMain
