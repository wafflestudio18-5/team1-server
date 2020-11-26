from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtokens.models import Token

from user.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'id',
            'firstName',
            'lastName',
            'email',
            'password',
        )

    