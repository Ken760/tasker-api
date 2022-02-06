# Generated by Django 3.2.9 on 2022-02-06 12:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(max_length=10000)),
                ('solutionText', models.TextField(blank=True, max_length=500, null=True)),
                ('uuid', models.SlugField(blank=True, max_length=160, unique=True)),
                ('isConfirmed', models.BooleanField(default=False)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('theme', models.CharField(choices=[('white', 'white'), ('red', 'red'), ('green', 'green'), ('blue', 'blue'), ('yellow', 'yellow')], default='White', max_length=50, null=True)),
                ('category', models.CharField(choices=[('algorithms', 'algorithms'), ('dataStructure', 'dataStructure'), ('architecture', 'architecture'), ('basics', 'basics')], max_length=50, null=True)),
                ('difficult', models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], max_length=50, null=True)),
                ('language', models.CharField(choices=[('CPlusPlus', 'CPlusPlus'), ('C', 'C'), ('CSharp', 'CSharp'), ('JavaScript', 'JavaScript'), ('Python', 'Python')], max_length=50, null=True)),
                ('followings', models.PositiveIntegerField(default=0, verbose_name='Переходы')),
                ('originalSource', models.CharField(blank=True, max_length=500, null=True)),
                ('code', models.TextField(blank=True, max_length=10000, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=5, null=True, verbose_name='Рейтинг')),
                ('userInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('task_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='tasker.task')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000, verbose_name='Сообщение')),
                ('task_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tasker.task')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
