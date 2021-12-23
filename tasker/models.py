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
    ("CPlusPlus", "C++"),
    ("C", "C"),
    ("CSharp", "C#"),
    ("JavaScript", "JavaScript"),
    ("Python", "Python"),
    ("Java", "Java"),
)


class Task(models.Model):
    """Задачи"""
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    text = models.TextField(max_length=500, blank=True, null=True)
    solution_text = models.TextField(max_length=500, blank=True, null=True, name='solutionText')
    uuid = models.SlugField(max_length=160, unique=True, blank=True)
    confirmed = models.BooleanField(default=False, name='isConfirmed')
    created_date = models.DateTimeField(auto_now_add=True, name='createdDate')
    updated_date = models.DateTimeField(auto_now=True, name='updatedDate')
    theme = models.CharField(max_length=50, choices=THEME, default='White', null=True)
    category = models.CharField(max_length=50, choices=CATEGORY, null=True)
    difficult = models.CharField(max_length=50, choices=DIFFICULT, null=True)
    language = models.CharField(max_length=50, choices=LANGUAGE, null=True)
    followings = models.PositiveIntegerField(default=0, verbose_name="Переходы")
    original_source = models.CharField(max_length=50, null=True, blank=True, name='originalSource')
    # rating = models.ForeignKey()
    # comments = models.ForeignKey('Comment', blank=True, null=True, on_delete=models.CASCADE)

    def save(self, **kwargs):
        if not self.id:
            self.uuid = uuid.uuid4().hex[:8]
        super().save(**kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Comment(models.Model):
    """Отзывы"""
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=1000)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Rating(models.Model):
    """Рейтинги"""
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='ratings', blank=True, null=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
