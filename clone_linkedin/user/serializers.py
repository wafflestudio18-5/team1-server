from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers, status, viewsets
from rest_framework.authtoken.models import Token
from django.db import transaction
from rest_framework.response import Response

from user.models import UserProfile, UserSchool, UserCompany, School

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
    firstName = serializers.SerializerMethodField()
    lastName = serializers.SerializerMethodField()
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
            'firstName',
            'lastName',
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

    def get_firstName(self, userprofile):
        user = userprofile.user
        return user.first_name

    def get_lastName(self, userprofile):
        user = userprofile.user
        return user.last_name


class UserSchoolSerializer(serializers.ModelSerializer):
    schoolName = serializers.CharField(source='school.name')
    startYear = serializers.IntegerField(required=False)
    endYear = serializers.IntegerField(required=False)
    major = serializers.CharField(required=False)

    class Meta:
        model = UserSchool
        fields = (
            'id',
            'schoolName',
            'startYear',
            'endYear',
            'major'
        )

    @transaction.atomic
    def update(self, userschool, school, validated_data):
        validated_data['school'] = school
        return super(UserSchoolSerializer, self).update(userschool, validated_data)


class UserCompanySerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(source='company.name')
    startDate = serializers.DateField(required=False)
    endDate = serializers.DateField(required=False)

    class Meta:
        model = UserSchool
        fields = (
            'id',
            'companyName',
            'startDate',
            'endDate'
        )

    @transaction.atomic
    def update(self, usercompany, company, validated_data):
        validated_data['company'] = company
        return super(UserCompanySerializer, self).update(usercompany, validated_data)

class GetProfileSerializer(serializers.ModelSerializer):

    firstName = serializers.CharField(source='user.first_name')
    lastName = serializers.CharField(source='user.last_name')
    region = serializers.CharField()
    contact = serializers.CharField()
    detail = serializers.CharField()
    school = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'firstName',
            'lastName',
            'region',
            'contact',
            'detail',
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

class UserDetailSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='user.first_name', required=False)
    lastName = serializers.CharField(source='user.last_name', required=False)
    detail = serializers.CharField(allow_blank=True)
    region = serializers.CharField(allow_blank=True)
    contact = serializers.CharField(allow_blank=True)

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'firstName',
            'lastName',
            'detail',
            'region',
            'contact'
        )

    @transaction.atomic
    def update(self, userprofile, validated_data):
        user_data = validated_data.pop('user')
        user = userprofile.user

        if user is not None:
            if bool('first_name' in user_data) and bool('last_name' in user_data):
                user.first_name = user_data['first_name']
                user.last_name = user_data['last_name']
                user.save()
            else:
                return Response({"error": "Can't update other User's profile"}, status=status.HTTP_400_BAD_REQUEST)

        userprofile.detail = validated_data.get('detail', userprofile.detail)
        userprofile.region = validated_data.get('region', userprofile.region)
        userprofile.contact = validated_data.get('contact', userprofile.contact)
        userprofile.save()
        return validated_data



class ShortUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'username'
        )
    def validate_password(self, value):
        return make_password(value)

    @transaction.atomic
    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = super(ShortUserSerializer, self).create(validated_data)
        Token.objects.create(user=user)

        return user


class UserNameSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
        )
    
    @transaction.atomic
    def update(self, user, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        user.first_name = first_name
        user.last_name = last_name
        return super(UserNameSerializer, self).update(user, validated_data)

class SocialSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False)
    username = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username'
        )