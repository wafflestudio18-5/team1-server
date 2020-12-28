from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from user.serializers import UserSerializer, UserNameSerializer, SocialSerializer
from django.conf import settings
from rest_framework.views import APIView
from google.auth.transport import requests
from google.oauth2 import id_token

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        if self.action in ('create', 'login'):
            return (AllowAny(), )
        return super(UserViewSet, self).get_permissions()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
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
        print(user)
        if user:
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")

            data = self.get_serializer(user).data
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
        return Response(self.get_serializer(user).data)

    def update(self, request, pk=None):
        if pk != 'me':
            return Response({"error": "Can't update other Users information"}, status=status.HTTP_403_FORBIDDEN)

        user = request.user
        data = request.data.copy()

        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        return Response(serializer.data, status = status.HTTP_200_OK)

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
        print(request.data)
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
            print(data)
            return Response(data, status=status.HTTP_201_CREATED)
        
        data = self.get_serializer(user).data
        token, _ = Token.objects.get_or_create(user=user)
        data['token'] = user.auth_token.key
        return Response(data, status=status.HTTP_200_OK)


