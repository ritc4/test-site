from http.client import HTTPResponse

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import JsonResponse


# Класс для вывода начальной странице
class HomeNews(ListView):
    model = News
    template_name = 'news/HomeNews.html'
    context_object_name = 'news'
    extra_context = {'title': 'Главная'}
    paginate_by = 2

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


# Класс для вывода с фильтром по категории
class CategoryNews(ListView):
    model = News
    template_name = 'news/home_category.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        # Вот так можно посматреть на что ссылается и сколько категорий
        # print([i.category.slug for i in self.model.objects.all()])
        # .select_related('category') это Функция которая собирает и выводит все зависимые SQL запросовы в шаблоне один раз
        return News.objects.filter(category__slug=self.kwargs['slug'], is_published=True).select_related('category')


# Класс для вывода конкретной новости
class ViewNews(DetailView):
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'news'


# Класс для работы с формами добавление новости после регистрации
class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    extra_context = {'title': 'Добавление новости'}
    # Если не указывать reverse_lazy django сам переходит по url указанный в model
    success_url = reverse_lazy('home')


# Класс для работы с формами Регистрация
# class RegisterUser(CreateView):
#     form_class = UserCreation
#     template_name = 'news/register.html'
#     # Если не указывать reverse_lazy django сам переходит по url указанный в model
#     success_url = reverse_lazy('login')
#
#     def form_valid(self,form):
#         messages.success(self.request, 'Вы успешно зарегистрировались')
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         messages.error(self.request, 'Ошибка регистрации')
#         return super().form_invalid(form)

# Класс для работы с формами Регистрация
class RegisterUser(CreateView):
    form_class = UserCreation
    template_name = 'news/register.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            username = request.POST.get('username')
            if User.objects.filter(username=username).exists():
                return JsonResponse(data={'text_resp': 'Пользователь с таким именем уже зарегистрирован'})
            elif username == '':
                return JsonResponse(data={'text_resp_error_text': 'Введите имя пользователя'})
            else:
                return JsonResponse(data={'text_resp_error': 'Имя свободно!'})
        else:
            return super().post(request, *args, **kwargs)

    def form_valid(self,form):
        messages.success(self.request, 'Вы успешно зарегистрировались')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка регистрации')
        return super().form_invalid(form)

# Класс для работы с формами Регистрация дополнения
# def UserValid(request):
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         username = request.POST.get('username')
#         if User.objects.filter(username=username).exists():
#             return JsonResponse(data={'text_resp': 'Пользователь с таким именем уже зарегистрирован'})
#         elif username == '':
#             return JsonResponse(data={'text_resp_error_text': 'Введите имя пользователя'})
#         else:
#             return JsonResponse(data={'text_resp_error': 'Имя свободно!'})


# Класс для работы с формами Авторизация
class LoginUser(LoginView):
    form_class = UserLogin
    template_name = 'news/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('home')


# Класс для работы с формами добавление новости после регистрации

class Send(FormView):
    form_class = Contact
    template_name = 'news/send_mail.html'
    extra_context = {'title': 'Связь с администрацией'}
    # Если не указывать reverse_lazy django сам переходит по url указанный в model
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        content = form.cleaned_data['content']
        send = send_mail(subject, content, 'ritc4@rambler.ru', ['ritc4mail@mail.ru'], fail_silently=False)
        if send == True:
            messages.success(self.request, 'Сообщение отправлено!')
        else:
            messages.success(self.request, 'Ошибка отправки сообщения!')
            return redirect('send')

        return super().form_valid(form)


# def form_valid(self, form):
#     if form.is_valid():
#         feedback = form.save(commit=False)
#         feedback.ip_address = get_client_ip(self.request)
#         if self.request.user.is_authenticated:
#             feedback.user = self.request.user
#         send_contact_email_message(feedback.subject, feedback.email, feedback.content, feedback.ip_address,
#                                    feedback.user_id)
#     return super().form_valid(form)

def form_invalid(self, form):
    messages.success(self.request, 'Ошибка заполнения формы, вы не верно ввели captcha!')
    return super().form_invalid(form)
