from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from blog.models import Post, Comment
from django.http import Http404
from .serializers import PostSerializer, CommentSerializer
from .pagination import PostLimitOffsetPagination


class PostListAPI(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostLimitOffsetPagination

    def get_queryset(self):
        queryset = Post.objects.all()

        # Special
        special = self.request.GET.get("special", "false")
        print(special)
        if str(special).lower() == "true":
            queryset = queryset.filter(special=True)
            print(queryset)

        # Search
        search_query = self.request.GET.get("q")
        if search_query:
            # Search by title
            queryset = queryset.filter(title__icontains=search_query)
        return queryset


class PostDetailAPI(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"


class CommentAPI(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return Comment.objects.filter(user=self.request.user, pk=self.kwargs.get('id'), deleted=False).first()

    def get_queryset(self):
        return Comment.objects.filter(post__pk=self.kwargs.get("post_id"), deleted=False)

    def destroy(self, request, *args, **kwargs):
        try:
            comment = self.get_object()
            comment.deleted = True
            comment.save()
        except:
            raise Http404
        return Response(status=200, data={"status": "ok", "msg": "Comment deleted"})

    def get_post_obj(self):
        try:
            post_id = self.kwargs['post_id']
            return Post.objects.get(pk=post_id)
        except:
            raise Http404

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        context = {
            'status': 'ok',
            'data': serializer.data,
        }
        return Response(context)

    def perform_create(self, serializer):
        saved = serializer.save(user=self.request.user, post=self.get_post_obj())
        return saved

