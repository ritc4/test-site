from django.db import models
from django.urls import reverse_lazy


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория', related_name='cat')

    def get_absolute_url(self):
        return reverse_lazy('view_news', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['category']
