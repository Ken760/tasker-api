# Generated by Django 3.2.9 on 2022-02-15 18:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20220215_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='joinedDate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
