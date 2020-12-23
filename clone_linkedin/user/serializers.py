from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user.models import UserProfile, UserSchool

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'firstName',
            'lastName',
            'email',
            'password',
        )


class UserProfileSerializer(serializers.ModelSerializer):
    region = serializers.CharField()
    contact = serializers.CharField()
    schoolName = serializers.CharField()
    schoolStartYear = serializers.IntegerField()
    schoolEndYear = serializers.IntegerField()
    major = serializers.CharField()
    companyName = serializers.CharField()
    companyStartDate = serializers.DateField()
    companyEndDate = serializers.DateField()

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'region',
            'contact',
            'schoolName',
            'schoolStartYear',
            'schoolEndYear',
            'major',
            'companyName',
            'companyStartDate',
            'companyEndDate'
        )
