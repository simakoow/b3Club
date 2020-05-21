"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .forms import Feedback
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog
from .models import Comment
from .forms import CommentForm
from .forms import BlogForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О Нас',
            'message':'Сведения о нас',
            'year':datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all() #запрос всех статей из модели
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts':posts, #передача списка статей в шаблон
            'year':datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blog page."""
    post_1 = Blog.objects.get(id=parametr) # запрос нужного поста
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit = False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)
            comment_f.save()

            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1':post_1, #передача конкретной статьи в шаблон веб страницы
            'comments' :comments,
            'form' :form,
            'year' :datetime.now().year,
        }
    )

def links (request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'message':'Переход по этим ссылкам поможет вам набраться опыта по ремонту, а так же послушать хорошую музыку во время этого!',
            'year':datetime.now().year,
        }
    )

def feedback(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1':'Мужчина', '2': 'Женщина'}
    usage = {'1':'Месяц','2':'Полгода',
            '3':'Год', '4':'Два года',
            '5':'Три года','6':'Четыре года',
            '7':'Пять и более лет'}
    if request.method == 'POST':
        form = Feedback(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['gender'] = gender[ form.cleaned_data['gender'] ]
            data['usage'] = usage[ form.cleaned_data['usage'] ]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = Feedback()
    return render(
        request,
        'app/feedback.html',
        {
            'form':form,
            'data':data
        }
    )

def registration(request):
    """Renders the registration page."""
    if request.method == "POST": # после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных
            return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    assert isinstance(request, HttpRequest)
    return render(
            request,
            'app/registration.html',
            {
                'regform': regform, # передача формы в шаблон веб-страницы
                'year':datetime.now().year,
            }
        )

def newpost(request):
    """Render the newpost page"""

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit = False)
            blog_f.posted = datetime.now()
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    assert isinstance (request, HttpRequest)
    return render(
        request,
        'app/newpost.html',
        {
            'blogform':blogform,
            'year':datetime.now().year,
        }
    )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'year':datetime.now().year,
        }
    )
