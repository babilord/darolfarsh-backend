from rest_framework import serializers
from blog.models import Post, Comment
from user_profile.api.serializers import UserPublicSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'user']
        read_only_fields = ['id', 'user']

    def get_user(self, obj):
        return UserPublicSerializer(obj.user).data


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'secondary_title', 'description', 'body', 'main_image', 'author', 'created', 'special', 'comments_count']

    def get_author(self, obj):
        return UserPublicSerializer(obj.author).data

    def get_comments_count(self, obj):
        return obj.comment_set.filter(deleted=False).count()
