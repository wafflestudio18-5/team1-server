from django.urls import include, path
from rest_framework.routers import SimpleRouter
from accounts.views import TokenViewSet


app_name = 'accounts'

router = SimpleRouter()
router.register('', TokenViewSet, basename='token') 

urlpatterns = [
    path('', include((router.urls))),
]