from rest_framework import serializers

from post.models import Post
# from user.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'createdAt',
            'updatedAt',
        )