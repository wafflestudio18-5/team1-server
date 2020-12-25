# import requests

# # from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView
# from rest_framework.authtoken.models import Token

# from allauth.socialaccount.providers.oauth2.views import (
#     OAuth2Adapter,
#     OAuth2CallbackView,
#     OAuth2LoginView,
# )

# from allauth.socialaccount.providers.google.provider import GoogleProvider

# class GoogleOAuth2Adapter(OAuth2Adapter):
#     provider_id = GoogleProvider.id
#     access_token_url = "https://accounts.google.com/o/oauth2/token"
#     authorize_url = "https://accounts.google.com/o/oauth2/auth"
#     profile_url = "https://www.googleapis.com/oauth2/v1/userinfo"

#     def complete_login(self, request, app, token, **kwargs):
#         resp = requests.get(
#             self.profile_url,
#             params={"access_token": token.token, "alt": "json"},
#         )

#         user = self.request.user
#         print(user)

#         resp.raise_for_status()
#         extra_data = resp.json()
#         login = self.get_provider().sociallogin_from_response(request, extra_data)

#         return login


# oauth2_login = OAuth2LoginView.adapter_view(GoogleOAuth2Adapter)
# oauth2_callback = OAuth2CallbackView.adapter_view(GoogleOAuth2Adapter)

# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter
#     client_class = OAuth2Client

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from user.serializers import UserSerializer


class TokenViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET'])
    def tokenize(self, request):
        user = request.user
        token, created = Token.objects.get_or_create(user=user)
        data['token'] = token.key
        return Response(data)
