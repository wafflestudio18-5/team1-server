from django.urls import include, path
from rest_framework.routers import SimpleRouter
from post.views import PostViewSet, CommentViewSet

app_name = 'post'

router = SimpleRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include((router.urls))),
]