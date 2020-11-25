# from django.shortcuts import render

from rest_framework import status, viewsets
# from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from post.serializers import PostSerializer
from post.models import Post

# Create your views here.

class PostViewSet(viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # GET /posts/
    def list(self, request):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)
    
    # POST /posts/
    def create(self, request):
        data = request.data.copy()  
        if data['content'] == '':
            return Response({"error": "The post cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
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
        if data['content'] == '':
            return Response({"error": "The post cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(post, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(post, serializer.validated_data)
        return Response(serializer.data)

    # DELETE /posts/:id/