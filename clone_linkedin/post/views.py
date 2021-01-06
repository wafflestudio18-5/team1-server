# from django.shortcuts import render

from rest_framework import status, viewsets, filters 
# from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from post.serializers import PostSerializer, PostDetailSerializer, PostReactionSerializer, CommentSerializer 
from post.models import Post, Comment

# Create your views here.

class PostViewSet(viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    search_fields = ['content']
    filter_backends = (filters.SearchFilter, )

    def get_serializer_class(self):
        if self.action == 'reaction':
            return PostReactionSerializer
        elif self.action == 'comment':
            return CommentSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        else:
            return PostSerializer

    # GET /posts/
    def list(self, request):
        queryset = self.get_queryset()
        param = request.query_params
        if param.get('order', '') == 'latest':
            queryset = queryset.order_by('-updatedAt')
        filter_backends = self.filter_queryset(queryset)
        page = self.paginate_queryset(filter_backends)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data) 

    # POST /posts/
    def create(self, request):
        data = request.data.copy()
        data['user_id'] = 1                      # Set user with id 1 as the one who wrote posts. Should be updated after login implemented.
        data['modified'] = False
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # GET /posts/:id/
    def retrieve(self, request, pk=None):
        post = self.get_object()
        return Response(self.get_serializer(post).data)

    # PUT /posts/:id/
    def update(self, request, pk=None):
        post = self.get_object()
        data = request.data.copy()
        data['modified'] = True
        serializer = self.get_serializer(post, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(post, serializer.validated_data)
        return Response(serializer.data)

    # DELETE /posts/:id/
    def destroy(self, request, pk=None):
        self.get_object().delete()
        return Response()
        
    # GET, POST, PUT, DELETE /posts/:id/reaction/
    @action(detail=True, methods=['GET', 'POST', 'PUT', 'DELETE'], url_path='reaction')
    def reaction(self, request, pk=None):
        post = self.get_object()
        data = request.data.copy()
        if self.request.method == 'GET':
            reaction = post.postReactions.all()
            return Response(self.get_serializer(reaction, many=True).data)
        elif self.request.method == 'POST':
            user = User.objects.get(id=1)          # Needs to be fixed after login implemented.
            if self.get_object().postReactions.filter(user=user).exists():
                return Response({"error": "Reaction already made."}, status=status.HTTP_400_BAD_REQUEST)
            data['user_id'] = 1
            data['post_id'] = post.id 
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif self.request.method == 'PUT':
            user = User.objects.get(id=1)          # Needs to be fixed after login implemented.
            reaction = get_object_or_404(post.postReactions, user=user)
            serializer = self.get_serializer(reaction, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.update(reaction, serializer.validated_data)
            return Response(serializer.data)     
        elif self.request.method == 'DELETE':
            user = User.objects.get(id=1)       # Needs to be fixed after login implemented.
            reaction = get_object_or_404(self.get_object().postReactions, user=user)     # Error if multiple reactions by the user exist
            reaction.delete()
            return Response()

    # POST /posts/:id/comment/
    @action(methods=['POST'], detail=True)
    def comment(self, request, pk=None):
        post = self.get_object()
        data = request.data.copy()
        data['user_id'] = 1                      # Set user with id 1 as the one who wrote comment. Should be updated after login implemented.
        data['post_id'] = post.id
        data['likes'] = 0
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentViewSet(viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # PUT /comment/:id/
    def update(self, request, pk=None):
        comment = self.get_object()
        data = request.data.copy()
        serializer = self.get_serializer(comment, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(comment, serializer.validated_data)
        return Response(serializer.data)

    # DELETE /comment/:id/
    def destroy(self, request, pk=None):
        self.get_object().delete()
        return Response()

