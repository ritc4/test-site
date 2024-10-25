from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Home_app.as_view(), name='home_app'),
    path('category/<str:slug>', Category_app.as_view(), name='category_app'),
]