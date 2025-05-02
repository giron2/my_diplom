from django.shortcuts import render
from posts.models import Post, Comment, Like
from rest_framework.response import Response
from posts.serializers import PostSerializer, PostDetailsSerializer, CommentSerializer, LikeSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import status
from django.db import models
from rest_framework import permissions
# Create your views here.
@api_view(['GET'])
def posts_list_view(request):
    post = Post.objects.all()
    serializer = PostSerializer(post, many=True)
    return Response(serializer.data)


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
class PostDetailsView(APIView):
    def get(self, request, id):
        posts = Post.objects.get(pk=id)
        ser = PostDetailsSerializer(posts, many=False)
        return Response(ser.data)

class PostViewSet(ModelViewSet):
    permission_classes = [IsCreatorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def get_permissions(self):
        if self.action in ["create"]:
            return [IsAuthenticated()]
        return [IsCreatorOrReadOnly()]


class CommentViewSet(ModelViewSet):
    permission_classes = [IsCreatorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get_permissions(self):
        if self.action in ["create"]:
            return [IsAuthenticated()]
        return [IsCreatorOrReadOnly()]


class LikeViewSet(ModelViewSet):
    permission_classes = [IsCreatorOrReadOnly]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    def get_permissions(self):
        if self.action in ["create"]:
            return [IsAuthenticated()]
        return [IsCreatorOrReadOnly()]

class LikeDetailsView(RetrieveAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
