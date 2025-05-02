from rest_framework import serializers
from posts.models import Post, Like, Comment
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, )
    class Meta:
        model = Comment
        fields = "__all__"
    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True,)
    class Meta:
        model = Post
        fields = ["author", 'id', 'image', 'text', 'created_at']
    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

class LikeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True,)
    class Meta:
        model = Like
        fields = ["author", 'id', 'in_stock', "post"]
    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
class PostDetailsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    like = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'image', 'text', 'created_at', 'comments', 'like']

    def get_like(self, obj):
        return obj.like.count()
