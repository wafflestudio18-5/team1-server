from rest_framework import serializers

from post.models import Post, PostReaction, Comment
# from user.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    # post_reactions = serializers.SerializerMethodField()
    # comments = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'createdAt',
            'updatedAt',
        )
    
    # def get_post_reactions(self, post):
    
    # def get_comments(self, post):

# class PostReactionSerializer(serializers.ModelSerializer):

# class CommentSerializer(serializers.ModelSerializer):