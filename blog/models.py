"""
Модели приложения blog.

- BlogPost — статья блога: заголовок, содержимое, превью, дата создания,
  признак публикации и счётчик просмотров.
"""

from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
        verbose_name="Превью (изображение)",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
