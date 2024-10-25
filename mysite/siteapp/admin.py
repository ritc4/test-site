from django.contrib import admin
from .models import Category,Article
from mptt.admin import DraggableMPTTAdmin


admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',),
    list_display_links=(
        'indented_title',),
    prepopulated_fields = {'slug':('name',)})

admin.site.register(Article)
