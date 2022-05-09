from rest_framework import serializers
from django.contrib.auth.models import User

from post.models import Post, Like


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(
        source='get_likes_count',
        read_only=True
    )
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'url', 'title', 'text', 'author', 'created', 'likes',)
        read_only_fields = ('created', 'id')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'url', 'post', 'created')
        read_only_fields = ('id', 'created')

    def get_queryset(self):
        return Like.objects.filter(author=self.request.user)
