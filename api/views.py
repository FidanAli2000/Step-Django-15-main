from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from blog.models import Post, Category, Tag
from .serializers import PostSerializer, CategorySerializer, TagSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer

    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.filter(is_active=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=["get"])
    def posts(self, request, pk=None):
        category = self.get_object()
        posts = category.posts.filter(is_published=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(methods=["get"], detail=True)
    def posts(self, request, pk=None):
        current_tag = self.get_object()
        published_posts = Post.objects.filter(tags=current_tag, is_published=True)
        data = PostSerializer(published_posts, many=True).data
        return Response(data)
