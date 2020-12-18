from django.urls import path
from accounts.views import GoogleLogin

app_name = 'accounts'
urlpatterns = [

    path(
        "login/google/",
        GoogleLogin.as_view(),
        name="google_login"
    ),
]