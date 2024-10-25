from django import template
from news.models import Category

register = template.Library()

@register.inclusion_tag('news/category_tags.html')
def show_category():
    category = Category.objects.all()
    return {'category':category}