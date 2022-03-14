import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


THEME = (
    ("white", "white"),
    ("red", "red"),
    ("green", "green"),
    ("blue", "blue"),
    ("yellow", "yellow"),
)
CATEGORY = (
    ("algorithms", "algorithms"),
    ("dataStructure", "dataStructure"),
    ("architecture", "architecture"),
    ("basics", "basics", )
)
DIFFICULT = (
    ("easy", "easy"),
    ("medium", "medium"),
    ("hard", "hard"),
)
LANGUAGE = (
    ("CPlusPlus", "CPlusPlus"),
    ("C", "C"),
    ("CSharp", "CSharp"),
    ("JavaScript", "JavaScript"),
    ("Python", "Python"),
)


class Task(models.Model):
    """Задачи"""
    user_info = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, name='userInfo')
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=10000)
    solution_text = models.TextField(max_length=500, blank=True, null=True, name='solutionText')
    solution_code = models.TextField(max_length=1000, blank=True, null=True, name='solutionCode')
    uuid = models.SlugField(max_length=160, unique=True, blank=True)
    confirmed = models.BooleanField(default=False, name='isConfirmed')
    created_date = models.DateTimeField(auto_now_add=True, name='createdDate')
    updated_date = models.DateTimeField(auto_now=True, name='updatedDate')
    theme = models.CharField(max_length=50, choices=THEME, default='White', null=True)
    category = models.CharField(max_length=50, choices=CATEGORY, null=True)
    difficult = models.CharField(max_length=50, choices=DIFFICULT, null=True)
    language = models.CharField(max_length=50, choices=LANGUAGE, null=True)
    followings = models.PositiveIntegerField(default=0, verbose_name="Переходы")
    original_source = models.CharField(max_length=500, null=True, blank=True, name='originalSource')
    code = models.TextField(max_length=10000, blank=True, null=True)

    def save(self, **kwargs):
        if not self.id:
            self.uuid = uuid.uuid4().hex[:8]
        super().save(**kwargs)

    def get_count_comments(self):
        return f"{self.comments.all().count()}"

    def get_count_likes(self):
        return f"{self.likes.count()}"

    def get_hasSelfLike(self):
        return self.likes.values_list('userInfo_id', 'userInfo__id')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Comment(models.Model):
    """Комментарии"""
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments', blank=True, null=True, name='taskId')
    user_info = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, name='userInfo')
    text = models.TextField("Сообщение", max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True, name='createdDate')
    updated_date = models.DateTimeField(auto_now=True, name='updatedDate')

    def __str__(self):
        return f"{self.text}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-createdDate']


class Like(models.Model):
    """Лайки"""
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, related_name='likes', name='taskId')
    user_info = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, name='userInfo')
    # value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"


class Favourite(models.Model):
    """Избранное"""
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, related_name='favourites',name='taskId')
    user_info = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, name='userInfo')

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"