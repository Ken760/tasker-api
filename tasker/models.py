import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings

THEME = (
    ("White", "White"),
    ("Red", "Red"),
    ("Green", "Green"),
    ("Blue", "Blue"),
    ("Yellow", "Yellow"),
)
CATEGORY = (
    ("Aлгоритмы", "Aлгоритмы"),
    ("Структуры данных", "Структуры данных"),
    ("Архитектура", "Архитектура"),
    ("Изучение основ языка", "Изучение основ языка", )
)
DIFFICULT = (
    ("easy", "easy"),
    ("medium", "medium"),
    ("hard", "hard"),
)
LANGUAGE = (
    ("C++", "C++"),
    ("C", "C"),
    ("C#", "C#"),
    ("JavaScript", "JavaScript"),
    ("Python", "Python"),
    ("Java", "Java"),
)


class Task(models.Model):
    """Задачи"""
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    text = models.TextField(max_length=500, blank=True, null=True)
    solution_text = models.TextField(max_length=500, blank=True, null=True)
    # url = models.SlugField(max_length=160, unique=True) #FIXME присвоить uuid
    confirmed = models.BooleanField(default=False, name='isConfirmed')
    created_date = models.DateTimeField(auto_now_add=True, name='createdDate')
    updated_date = models.DateTimeField(auto_now=True, name='updatedDate')
    theme = models.CharField(max_length=50, choices=THEME, default='White', null=True)
    category = models.CharField(max_length=50, choices=CATEGORY, null=True)
    difficult = models.CharField(max_length=50, choices=DIFFICULT, null=True)
    # rating = models.ForeignKey()
    # comments = models.ForeignKey('Comment', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Comment(models.Model):
    """Отзывы"""
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=1000)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Rating(models.Model):
    """Рейтинги"""
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
