# from django.shortcuts import render

from rest_framework import status, viewsets
# from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from post.serializers import PostSerializer, PostDetailSerializer, PostReactionSerializer 
from post.models import Post

# Create your views here.

class PostViewSet(viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action == 'reaction':
            return PostReactionSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        else:
            return PostSerializer

    # GET /posts/
    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    # POST /posts/
    def create(self, request):
        data = request.data.copy()
        data['user_id'] = 1                      # Set user with id 1 as the one who wrote posts. Should be updated after login implemented.
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
            reaction = self.get_object().postReactions
            return Response(self.get_serializer(reaction).data)
        elif self.request.method == 'POST':
            data['user_id'] = 1
            data['post_id'] = post.id 
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif self.request.method == 'PUT':
            serializer = self.get_serializer(data=data) 
            serializer.is_valid(raise_exception=True) 
            serializer.update(serializer.validated_data)
            return Response(serializer.data) 
        elif self.request.method == 'DELETE':
            self.get_object().delete()
            return Response() 
        