from rest_framework import serializers

from django.contrib.auth.models import User
from post.models import Post, PostReaction, Comment
# from user.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user.id', read_only=True)
    userFirstName = serializers.CharField(source='user.first_name', read_only=True)
    userLastName = serializers.CharField(source='user.last_name', read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'createdAt',
            'updatedAt',
            'userId',
            'userFirstName',
            'userLastName',
            'user_id',
        )

    def create(self, validated_data):
        validated_data['user'] = User.objects.get(id=validated_data.pop('user_id'))
        return super(PostSerializer, self).create(validated_data)

    # def get_post_reactions(self, post):
    
    # def get_comments(self, post):

# class PostReactionSerializer(serializers.ModelSerializer):

# class CommentSerializer(serializers.ModelSerializer):