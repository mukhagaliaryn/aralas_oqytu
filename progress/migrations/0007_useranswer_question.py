# Generated by Django 5.1.4 on 2025-01-11 17:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_framecontent_url'),
        ('progress', '0006_delete_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.question', verbose_name='Сұрақ'),
        ),
    ]
