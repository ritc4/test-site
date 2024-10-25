from django.views.generic import ListView, DetailView
from .models import *


class Home_app(ListView):
    model = Category
    template_name = 'siteapp/home_app.html'
    context_object_name = 'home'


class Category_app(ListView):
    model = Category
    template_name = 'siteapp/category_app.html'
    context_object_name = 'category'

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_category = Category.objects.get(slug=self.kwargs['slug'])
        context['selected_category'] = selected_category

        # предки
        ances = selected_category.get_ancestors()
        context['ances'] = ances

        # все потомки
        # descendants = selected_category.get_descendants()
        # cats = [i.slug for i in descendants]
        # cats.append(self.kwargs['slug'])

        # context['des'] = cats
        # print(cats)

        article = Article.objects.filter(category__slug=self.kwargs['slug']).select_related('category')
        context['article'] = article

        # потомки
        children = selected_category.get_children()
        context['children'] = children

        # Предки + модель + потомки
        # family = selected_category.get_family()

        # следующий родственный элемент
        # next = selected_category.get_next_sibling()

        # получение корневой узел дерева
        # root = selected_category.get_root()
        # context['root'] = root

        # print(root)
        return context
