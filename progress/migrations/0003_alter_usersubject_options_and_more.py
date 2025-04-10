# Generated by Django 5.1.4 on 2025-01-08 19:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0002_usersubject_completed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usersubject',
            options={'verbose_name': 'Қолданушының пәні', 'verbose_name_plural': 'Қолданушылардың пәндері'},
        ),
        migrations.AlterField(
            model_name='userlesson',
            name='user_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_lessons', to='progress.usersubject', verbose_name='Қолданушының пәні'),
        ),
    ]
