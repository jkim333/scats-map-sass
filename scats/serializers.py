from rest_framework import serializers
from .models import Scats


class ScatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scats
        fields = '__all__'
