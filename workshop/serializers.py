from rest_framework import serializers
from .models.users import User
from .models import Workshop

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'type', 'studio_name', 'studio_location', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'
