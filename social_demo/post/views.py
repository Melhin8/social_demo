from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

from post.models import Post, Like
from post.serializers import UserSerializer, PostSerializer, LikeSerializer
from post.mixins import AutofillAuthorMixin
from post.permissions import IsAuthorPermission


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SignupUserView(CreateAPIView):
    model = User
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class PostViewSet(AutofillAuthorMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorPermission)


class LikeViewSet(AutofillAuthorMixin, viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorPermission)
