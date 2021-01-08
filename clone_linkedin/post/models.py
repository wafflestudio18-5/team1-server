from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to="%Y/%m/%d", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    modified = models.BooleanField(default=False)

class PostReaction(models.Model):
    LIKE = 'Like'
    CELEBRATE = 'Celebrate'
    SUPPORT = 'Support'
    LOVE = 'Love'
    INSIGHTFUL = 'Insightful'
    CURIOUS = 'Curious'

    TYPE_CHOICES = (
        (LIKE, LIKE),
        (CELEBRATE, CELEBRATE),
        (SUPPORT, SUPPORT),
        (LOVE, LOVE),
        (INSIGHTFUL, INSIGHTFUL),
        (CURIOUS, CURIOUS),
    )

    TYPES = (LIKE, CELEBRATE, SUPPORT, LOVE, INSIGHTFUL, CURIOUS)

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=LIKE)
    # Many-to-one relationship between PostReaction and Post
    post = models.ForeignKey(Post, related_name = "postReactions", on_delete=models.CASCADE)
    # Many-to-one relationship between PostReaction and User 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    # Many-to-one relationship between Comment and Post
    post = models.ForeignKey(Post, related_name = "comments", on_delete=models.CASCADE)
    # Many-to-one relationship between Comment and User 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.PositiveSmallIntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

