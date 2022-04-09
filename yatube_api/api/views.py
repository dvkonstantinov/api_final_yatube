from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .serializers import (PostSerializer, CommentSerializer,
                          GroupSerializer, FollowSerializer)
from posts.models import Post, Group, Comment, Follow
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=pk)
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        pk = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=pk)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        user = self.request.user
        # Не совсем понимаю, при чем тут related_name? Мы же фильтруем по
        # столбцу user_id и ищем все записи по текущему пользователю
        return Follow.objects.filter(user=user)
