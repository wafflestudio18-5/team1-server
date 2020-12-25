from rest_framework import serializers

from django.contrib.auth.models import User
from post.models import Post, PostReaction, Comment
# from user.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user.id', read_only=True)
    userFirstName = serializers.CharField(source='user.first_name', read_only=True)
    userLastName = serializers.CharField(source='user.last_name', read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    userSchool = serializers.SerializerMethodField()
    userCompany = serializers.SerializerMethodField

    class Meta:
        model = Post
        fields = (
            'id',
            'content',
            'createdAt',
            'updatedAt',
            'modified',
            'userId',
            'userFirstName',
            'userLastName',
            'user_id',
            'userSchool',
        )

    def create(self, validated_data):
        validated_data['user'] = User.objects.get(id=validated_data.pop('user_id'))
        return super(PostSerializer, self).create(validated_data)

    def get_userSchool(self, post):
        userSchools = post.user.linkedin_user.userschool_set
        if not userSchools.exists():
            return None
        return userSchools.latest('endYear', 'startYear')[0]

class PostDetailSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user.id')
    userFirstName = serializers.CharField(source='user.first_name')
    userLastName = serializers.CharField(source='user.last_name')
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'content',
            'createdAt',
            'updatedAt',
            'modified',
            'userId',
            'userFirstName',
            'userLastName',
            'comments',
        )

    # def get_post_reactions(self, post):
    
    def get_comments(self, post):
        return CommentSerializer(post.comments, many=True).data

# class PostReactionSerializer(serializers.ModelSerializer):

class CommentSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user.id', read_only=True)
    userFirstName = serializers.CharField(source='user.first_name', read_only=True)
    userLastName = serializers.CharField(source='user.last_name', read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    post_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'likes',
            'createdAt',
            'updatedAt',
            'userId',
            'userFirstName',
            'userLastName',
            'createdAt',
            'updatedAt',
            'user_id',
            'post_id',
        )

    def create(self, validated_data):
        validated_data['user'] = User.objects.get(id=validated_data.pop('user_id'))
        validated_data['post'] = Post.objects.get(id=validated_data.pop('post_id'))
        return super(CommentSerializer, self).create(validated_data)
