from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(null=False, blank=False, max_length=350)
    secondary_title = models.CharField(null=True, blank=True, max_length=600)
    description = models.TextField(null=True, blank=True, max_length=1000)
    body = models.TextField(null=False, blank=False, max_length=10000)
    main_image = models.ImageField(null=True, blank=True, upload_to="blog")
    author = models.ForeignKey(User, null=False, blank=False, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    special = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " by " + self.author.username


class Comment(models.Model):
    text = models.TextField(null=False, blank=False, max_length=1500)
    post = models.ForeignKey(Post, null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.post.title
