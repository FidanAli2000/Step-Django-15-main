from rest_framework import serializers

from blog.models import Category, Comment, Post, Tag


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = ["id", "author", "author_name", "text", "created_at", "parent"]
        read_only_fields = ["created_at"]


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source="author.username")
    category_name = serializers.ReadOnlyField(source="category.name")
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "title", "author", "author_name", "category", "category_name", "tags",
            "content", "image", "is_published", "views", "created_at",
            "like_count", "comment_count", "comments",
        ]
        read_only_fields = ["views", "created_at"]

    def get_like_count(self, post):
        return post.likes.count()

    def get_comment_count(self, post):
        active_comments = post.comments.filter(is_active=True)
        return active_comments.count()

    def get_comments(self, post):
        active_comments = post.comments.filter(is_active=True)
        return CommentSerializer(active_comments, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description", "post_count")

    def get_post_count(self, category):
        published_posts = category.posts.filter(is_published=True)
        return published_posts.count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]
