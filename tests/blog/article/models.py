from django.contrib.auth.models import User
from django.db import models


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Article(DateMixin):
    title = models.CharField(max_length=200)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(DateMixin):
    message = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
