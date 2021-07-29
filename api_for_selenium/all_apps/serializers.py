from rest_framework import serializers


class UserDataSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    email = serializers.EmailField(max_length=200, required=True)
    password = serializers.CharField(max_length=2000, required=True)
    phone_number = serializers.CharField(max_length=1000, required=True)
    address = serializers.CharField(max_length=1000, required=True)

