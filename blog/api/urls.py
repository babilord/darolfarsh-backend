from django.urls import path
from .views import PostListAPI, PostDetailAPI, CommentAPI

app_name = "blog-api"
urlpatterns = [
    path('posts/', PostListAPI.as_view(), name="posts-list"),
    path('post/<int:id>/', PostDetailAPI.as_view(), name="post-detail"),
    path('post/<int:post_id>/comments/', CommentAPI.as_view({'get': 'list'}), name="post-comments"),
    path('post/<int:post_id>/comment/create/', CommentAPI.as_view({'post': 'create'}), name="post-comment-create"),
    path('comment/<int:id>/delete/', CommentAPI.as_view({'delete': 'destroy'}), name="comment-delete"),
]
