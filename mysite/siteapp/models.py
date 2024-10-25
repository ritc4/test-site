from django.db import models
from django.urls import reverse_lazy
from mptt.models import MPTTModel,TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=255,verbose_name='Url',unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('category_app', kwargs={'slug': self.slug})

    class MPTTMeta:
        order_insertion_by = ['name']


class Article(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    category = TreeForeignKey(Category,on_delete=models.PROTECT)

    def __str__(self):
        return self.name