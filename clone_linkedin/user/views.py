from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from user.models import School, UserSchool, UserProfile, UserCompany, Company

from user.serializers import UserSerializer, UserProfileSerializer, GetProfileSerializer

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        return (AllowAny(), )

    def get_serializer_class(self):
        if self.action == 'profile' and self.request.method == 'POST':
            print("POST!!\n")
            return UserProfileSerializer
        elif self.action == 'profile' and self.request.method == 'GET':
            print("GET!!\n")
            return GetProfileSerializer
        elif self.action == 'profile' and self.request.method == 'PUT':
            print("PUT!!\n")
            return UserProfileSerializer
        else:
            return UserSerializer

    @action(detail=False, methods=['POST', 'GET'])
    def profile(self, request):
        if self.request.method == 'POST':
            return self._create_profile(request)
        elif self.request.method == 'GET':
            return self._get_profile(request)
        else:
            return self._update_profile(request)

    # GET /user/profile/
    def _get_profile(self, request):
        user = User.objects.get(id=1)
        userprofile = UserProfile.objects.get(user=user.id)
        data = GetProfileSerializer(userprofile).data
        return Response(data, status=status.HTTP_200_OK)


    # POST /user/profile/
    def _create_profile(self, request):
        user = User.objects.get(id=1) # 토큰 발급 후에 수정해야함.
        data = request.data.copy()
        userProfile = UserProfile.objects.get(user_id=user)

        # school
        schoolName = data['schoolName']
        startyear = data['schoolStartYear']
        endyear = data['schoolEndYear']
        major = data['major']
        school, is_school = School.objects.get_or_create(name=schoolName)
        userschool = UserSchool.objects.create(userProfile=userProfile, school=school,
                                               startYear=startyear, endYear=endyear, major=major)

        #company
        companyName = data['companyName']
        startdate = data['companyStartDate']
        enddate = data['companyEndDate']
        company, is_company = Company.objects.get_or_create(name=companyName)
        usercompany = UserCompany.objects.create(userProfile=userProfile, company=company,
                                                 startDate=startdate, endDate=enddate)

        return Response(data, status=status.HTTP_201_CREATED)

    # PUT /user/profile/
    def _update_profile(self, request):
        user = User.objects.get(id=1) # 토큰 발급 후에 수정해야함.
        data = request.data.copy()
        userProfile = UserProfile.objects.get(user_id=user)

        #school
        schoolName = data['schoolName']
        startyear = data['schoolStartYear']
        endyear = data['schoolEndYear']
        major = data['major']
        school, is_school = School.objects.get_or_create(name=schoolName)
        userschool = UserSchool.object.filter(userProfile=userProfile, school=school).first()

        return Response(data, status=status.HTTP_200_OK)


