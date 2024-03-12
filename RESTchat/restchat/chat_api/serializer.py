from rest_framework import serializers
from chatrooms.models import Chat
from django.contrib.auth.models import User


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('name', 'slug')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
