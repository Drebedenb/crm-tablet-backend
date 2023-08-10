from rest_framework import serializers
from .models import WorkersMain


class WorkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkersMain
        fields = ['UserLogin', 'UserPassword', 'ShortName']