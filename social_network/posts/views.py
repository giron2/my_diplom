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
# Create your views here.
@api_view(['GET'])
def posts_list_view(request):
    post = Post.objects.all()
    serializer = PostSerializer(post, many=True)
    return Response(serializer.data)

class PostDetailsView(APIView):
    def get(self, request, id):
        posts = Post.objects.get(pk=id)
        ser = PostDetailsSerializer(posts, many=False)
        return Response(ser.data)

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        return []

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        return []

class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class LikeDetailsView(RetrieveAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
