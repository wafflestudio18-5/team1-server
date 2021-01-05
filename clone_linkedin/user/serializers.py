from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user.models import UserProfile, UserSchool, UserCompany

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
    image = serializers.ImageField(use_url=True) 
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
            'image',
            'schoolName',
            'schoolStartYear',
            'schoolEndYear',
            'major',
            'companyName',
            'companyStartDate',
            'companyEndDate'
        )

class UserSchoolSerializer(serializers.ModelSerializer):
    schoolName = serializers.SerializerMethodField()
    startYear = serializers.IntegerField()
    endYear = serializers.IntegerField()
    major = serializers.CharField()

    class Meta:
        model = UserSchool
        fields = (
            'id',
            'schoolName',
            'startYear',
            'endYear',
            'major'
        )

    def get_schoolName(self, userschool):
        return userschool.school.name


class UserCompanySerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(source='company.name')
    startDate = serializers.DateField()
    endDate = serializers.DateField()

    class Meta:
        model = UserSchool
        fields = (
            'id',
            'companyName',
            'startDate',
            'endDate'
        )

class GetProfileSerializer(serializers.ModelSerializer):
    region = serializers.CharField()
    contact = serializers.CharField()
    school = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'region',
            'contact',
            'school',
            'company'
        )

    def get_school(self, user):
        userprofile = UserProfile.objects.get(id=user.id)
        schools = UserSchool.objects.filter(userProfile=userprofile)
        return UserSchoolSerializer(schools, many=True, context=self.context).data

    def get_company(self, user):
        userprofile = UserProfile.objects.get(id=user.id)
        companies = UserCompany.objects.filter(userProfile=userprofile)
        return UserCompanySerializer(companies, many=True, context=self.context).data