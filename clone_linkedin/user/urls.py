from django.urls import include, path
from rest_framework.routers import SimpleRouter

from user.views import UserViewSet, UserNameViewSet

app_name = 'user'

router = SimpleRouter()
router.register('user', UserViewSet, basename='user') 
router.register('username', UserNameViewSet, basename='username')


urlpatterns = [
    path('', include((router.urls))),
]
