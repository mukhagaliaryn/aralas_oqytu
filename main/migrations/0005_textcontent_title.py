# Generated by Django 5.1.4 on 2025-01-09 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_framecontent_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='textcontent',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Тақырыбы'),
        ),
    ]
