"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your models here.

# Модель данных Блога – class Blog
class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")

    # Методы класса:
    def get_absolute_url(self): # метод возвращает строку с URL-адресом записи
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self): # метод возвращает название, используемое для представления отдельных записей в административном разделе
        return self.title

    # Метаданные – вложенный класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = 'Posts' # имя таблицы для модели
        ordering = ['-posted'] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "статья блога" # имя, под которым модель будет отображаться в административном разделе (для одной статьи блога)
        verbose_name_plural = "статьи блога" # тоже для всех статей блога

admin.site.register(Blog)

#Модель комментария

class Comment(models.Model):
    text = models.TextField(verbose_name = "Комментарий")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата")
    author = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name = "Автор")
    post = models.ForeignKey(Blog, on_delete= models.CASCADE, verbose_name = "Статья")

    #Методы класса
    def _str_(self):
        return 'Комментарий %s к %s' % (self.author, self.post)

    #Метаданые
    class Meta:
        db_table = "Comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии к статьям блога"
        ordering= ['-date']

admin.site.register(Comment)