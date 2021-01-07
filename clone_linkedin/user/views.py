from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from user.models import School, UserSchool, UserProfile, UserCompany, Company

from user.serializers import UserSerializer, UserProfileSerializer, GetProfileSerializer, \
                             UserSchoolSerializer, UserCompanySerializer, \
                             ShortUserSerializer, UserNameSerializer, SocialSerializer, UserDetailSerializer

from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        if self.action in ('logout', 'get', 'update', 'profile',
                           'school', 'company', 'specific', 'newschool', 'newcompany'):
            return super(UserViewSet, self).get_permissions()
        return (AllowAny(), )
    
    def create(self, request):
        serializer = ShortUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        data = serializer.data
        data['token'] = user.auth_token.key
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['PUT'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")

            data = ShortUserSerializer(user).data
            token, created = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            return Response(data, status = status.HTTP_200_OK)

        return Response({"error": "Wrong email or wrong password"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        logout(request)
        return Response(status = status.HTTP_200_OK)

    def get(self, request, pk=None):
        user = request.user
        return Response(ShortUserSerializer(user).data)

    def update(self, request, pk = None):
        user = request.user
        data = request.data.copy()

        serializer = ShortUserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'profile' and self.request.method == 'POST':
            return UserProfileSerializer
        elif self.action == 'profile' and self.request.method == 'GET':
            return GetProfileSerializer
        elif self.action == 'profile' and self.request.method == 'PUT':
            return UserProfileSerializer
        elif self.action == 'school' or self.action == 'newschool':
            return UserSchoolSerializer
        elif self.action == 'company' or self.action == 'newcompany':
            return UserCompanySerializer
        elif self.action == 'specific':
            return UserDetailSerializer
        else:
            return UserSerializer

    @action(detail=True, methods=['GET'])
    def profile(self, request, pk=None):
        if pk == 'me':
            user = request.user
        else:
            user = User.objects.get(id=pk)


        userprofile, is_userprofile = UserProfile.objects.get_or_create(user=user)
        data = GetProfileSerializer(userprofile).data
        return Response(data, status=status.HTTP_200_OK)


    # /user/me/profile/specific/
    @action(detail=True, methods=['GET', 'PUT'], url_path='profile/specific')
    def specific(self, request, pk=None):
        if pk != 'me':
            return Response({"error": "Can't update other User's profile"}, status=status.HTTP_403_FORBIDDEN)

        user = request.user
        userprofile = UserProfile.objects.get(user=user.id)

        if self.request.method == 'PUT':
            return self._update_specific(request, user, userprofile)

        else:
            return self._get_specific(request, userprofile)

    def _get_specific(self, request, userprofile):
        serializer = self.get_serializer(userprofile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _update_specific(self, request, user, userprofile):
        data = request.data.copy()
        serializer = self.get_serializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_data = serializer.update(userprofile, serializer.validated_data)
        updated_serializer = self.get_serializer(data=data)
        updated_serializer.is_valid(raise_exception=True)
        return Response(updated_serializer.data, status=status.HTTP_200_OK)

    # /user/me/profile/newschool/
    @action(detail=True, methods=['POST'], url_path='profile/newschool')
    def newschool(self, request, pk=None):
        if pk != 'me':
            return Response({"error": "Can't update other User's profile"}, status=status.HTTP_403_FORBIDDEN)
        user = request.user
        data = request.data.copy()
        schoolName = data['schoolName']

        userprofile = UserProfile.objects.get(user=user.id)
        school, is_school = School.objects.get_or_create(name=schoolName)
        userschool = UserSchool.objects.create(userProfile=userprofile, school=school)
        serializer = self.get_serializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(userschool, school, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['GET', 'PUT', 'DELETE'], url_path='profile/school/(?P<school_pk>[^/.]+)')
    def school(self, request, pk=None, school_pk=None):
        if pk != 'me':
            return Response({"error": "Can't update other User's profile"}, status=status.HTTP_403_FORBIDDEN)

        user = request.user
        userprofile = UserProfile.objects.get(user=user.id)
        if UserSchool.objects.get(id=school_pk).userProfile != userprofile:
            return Response({"error": "This profile is not your one"}, status=status.HTTP_400_BAD_REQUEST)
        userschool = UserSchool.objects.get(userProfile=userprofile, id=school_pk)

        if self.request.method == 'PUT':
            return self._update_school(request, userschool, userprofile, school_pk)
        elif self.request.method == 'DELETE':
            return self._delete_school(request, userschool)
        elif self.request.method == 'GET':
            return self._get_school(request, userschool)

    # GET /user/me/profile/school/:id/
    def _get_school(self, request, userschool):
        serializer = self.get_serializer(userschool)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT /user/me/profile/school/:id/
    def _update_school(self, request, userschool, userprofile, school_pk):
        data = request.data.copy()
        schoolName = data['schoolName']
        startyear = data['startYear']
        endyear = data['endYear']
        major = data['major']
        school, is_school = School.objects.get_or_create(name=schoolName)
        UserSchool.objects.filter(id=userschool.id).update(school_id=school.id, startYear=startyear, endYear=endyear, major=major)
        updatedUserSchool = UserSchool.objects.get(userProfile=userprofile, id=school_pk)
        serializer = self.get_serializer(updatedUserSchool)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE /user/me/profile/school/:id/
    def _delete_school(self, request, userschool):
        userschool.delete()
        return Response()

    # POST /user/me/profile/newcompany/
    @action(detail=True, methods=['POST'], url_path='profile/newcompany')
    def newcompany(self, request, pk=None):
        if pk != 'me':
            return Response({"error": "Can't update other User's profile"}, status=status.HTTP_403_FORBIDDEN)

        user = request.user
        data = request.data.copy()
        companyName = data['companyName']
        userprofile = UserProfile.objects.get(user=user.id)
        company, is_company = Company.objects.get_or_create(name=companyName)
        usercompany = UserCompany.objects.create(userProfile=userprofile, company=company)
        serializer = self.get_serializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(usercompany, company, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET', 'PUT', 'DELETE'], url_path='profile/company/(?P<company_pk>[^/.]+)')
    def company(self, request, pk=None, company_pk=None):
        if pk != 'me':
            return Response({"error": "Can't update other User's profile"}, status=status.HTTP_403_FORBIDDEN)

        user = request.user

        userprofile = UserProfile.objects.get(user=user.id)
        if UserCompany.objects.get(id=company_pk).userProfile != userprofile:
            return Response({"error": "This profile is not your one"}, status=status.HTTP_400_BAD_REQUEST)
        usercompany = UserCompany.objects.get(userProfile=userprofile, id=company_pk)

        if self.request.method == 'PUT':
            return self._update_company(request, usercompany, userprofile, company_pk)
        elif self.request.method == 'DELETE':
            return self._delete_company(request, usercompany)
        else:
            return self._get_company(request, usercompany)

    def _get_company(self, request, usercompany):
        serializer = self.get_serializer(usercompany)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _update_company(self, request, usercompany, userprofile, company_pk):
        data = request.data.copy()
        companyName = data['companyName']
        startdate = data['startDate']
        enddate = data['endDate']
        company, is_company = Company.objects.get_or_create(name=companyName)
        UserCompany.objects.filter(id=usercompany.id).update(company=company, startDate=startdate, endDate=enddate)
        updatedUserCompany = UserCompany.objects.get(userProfile=userprofile, id=company_pk)
        serializer = self.get_serializer(updatedUserCompany)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _delete_company(self,request, usercompany):
        usercompany.delete()
        return Response()



class UserNameViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserNameSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        return super(UserNameViewSet, self).get_permissions()

    def update(self, request, pk = None):
        user = request.user
        data = request.data.copy()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.update(user, serializer.validated_data)

        return Response(serializer.data, status = status.HTTP_200_OK)

class SocialLoginViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SocialSerializer
    
    @action(detail=False, methods=['POST'])
    @permission_classes((AllowAny,))
    def login(self, request):
        client_id = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        idinfo = id_token.verify_oauth2_token(request.data['tokenId'], requests.Request(), client_id)

        try:
            user = User.objects.get(email=idinfo['email'])
        except:
            data = {}
            data['email'] = idinfo['email']
            data['username'] = idinfo['email']

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")

            token, _ = Token.objects.get_or_create(user=user)
            data['token'] = user.auth_token.key
            return Response(data, status=status.HTTP_201_CREATED)
        
        data = self.get_serializer(user).data
        token, _ = Token.objects.get_or_create(user=user)
        data['token'] = user.auth_token.key
        return Response(data, status=status.HTTP_200_OK)

