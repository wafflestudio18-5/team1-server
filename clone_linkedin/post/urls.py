from django.urls import include, path
from rest_framework.routers import SimpleRouter
from post.views import PostViewSet

app_name = 'post'

router = SimpleRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include((router.urls))),
]