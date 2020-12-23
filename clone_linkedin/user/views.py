from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from user.models import School, UserSchool, UserProfile, UserCompany, Company

from user.serializers import UserSerializer, UserProfileSerializer

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        return (AllowAny(), )

    def get_serializer_class(self):
        if self.action == 'profile':
            return UserProfileSerializer
        else:
            return UserSerializer



    # POST /user/profile/
    @action(detail=False, methods=['POST'])
    def profile(self, request):
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
                                                 startDate = startdate, endDate=enddate)

        return Response(data, status=status.HTTP_201_CREATED)

