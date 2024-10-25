from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.views.decorators.cache import cache_page

urlpatterns = [
    # Пример кэширование страниц в файл
    # path('',cache_page(60)(HomeNews.as_view()),name='home'),
    path('',HomeNews.as_view(),name='home'),
    path('category/<str:slug>',CategoryNews.as_view(),name='category'),
    path('view_category/<str:slug>',ViewNews.as_view(),name='view_news'),
    path('add_news/',CreateNews.as_view(),name='add_news'),
    path('register/',RegisterUser.as_view(),name='register'),
    path('login/',LoginUser.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('send_email/',Send.as_view(),name='send'),
    # path('user_valid/',UserValid,name='user_valid'),
]
