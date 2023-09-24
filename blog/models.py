from django.db import models
from users.models import User


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Содержимое')
    slug = models.CharField(max_length=200, null=True, blank=True, verbose_name="slug")
    content = models.TextField(max_length=500)
    preview_image = models.ImageField(upload_to='blog_previews/')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
