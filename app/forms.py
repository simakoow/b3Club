"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class Feedback(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length= 30)
    city = forms.CharField(label='Ваш город', min_length=2, max_length=30)
    gender = forms.ChoiceField(label='Ваш пол',
                               choices=[('1','Мужчина'), ('2','Женщина')],
                               widget=forms.RadioSelect, initial=1)
    usage = forms.ChoiceField(label='Как давно вы владеете passat b3?',
                               choices=(('1','Месяц'),
                               ('2','Полгода'),
                               ('3','Год'),
                               ('4','Два года'),
                               ('5', 'Три года'),
                               ('6','Четыре года'),
                               ('7','Пять и более лет')),initial = 1)
    notice = forms.BooleanField(label='Хотите чтоб мы ответили вам на e-mail?',
                                required = False)
    email = forms.EmailField(label='Ваш e-mail', min_length=10)
    message = forms.CharField(label='Текст сообщения', 
                              widget=forms.Textarea(attrs={'rows':12,'cols':20}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text' : "Комментарий"}

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'posted', 'author', 'image',)
        labels = {'title':"Заголовок", 'description':"Краткое описание", 'content':"Содержание", 'posted':"Дата", 'author':"Автор", 'image':"Изображение",}
