from django import forms
from .models import Category, News
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

# Кастомный валидатор
import re
from django.core.exceptions import ValidationError


# Форма не связанная с моделями только category
# class NewsForm(forms.Form):
#     title = forms.CharField(max_length=150,label='Название',widget=forms.TextInput(attrs={'class': 'form-control'}))
#     content = forms.CharField(label='Текст',required=False,widget=forms.Textarea(attrs={'class': 'form-control','rows':5}))
#     is_published = forms.BooleanField(label='Опубликовано?',initial=True)
#     category = forms.ModelChoiceField(empty_label='Выберите категорию', queryset=Category.objects.all(),label='Категория',widget=forms.Select(attrs={'class': 'form-control'}))

# Форма связаная с моделью
class NewsForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Выберите категорию",
                                      label='Категории')

    class Meta:
        model = News
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}, ),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}, ),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    # Кастомный валидатор
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинатся с цифры')
        return title


class UserCreation(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',help_text='максимум 150 символов',widget=forms.TextInput(attrs={'class': 'form-control','autocomplete':'off'},))
    email = forms.EmailField(label='Почта',widget=forms.EmailInput(attrs={'class': 'form-control'},))
    password1 = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class': 'form-control'},))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'},))

    class Meta:
        model = User
        fields = ('username','email','password1','password2')


class UserLogin(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', help_text='максимум 150 символов',widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'},))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'},))


class Contact(forms.Form):
    subject = forms.CharField(label='Тема',widget=forms.TextInput(attrs={'class': 'form-control'}, ))
    content = forms.CharField(label='Текс',widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}, ))
    captcha = CaptchaField()

    # class Meta:
    #     model = UserCreation
    #     fields = ('subject','content')