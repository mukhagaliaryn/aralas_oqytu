# Generated by Django 5.1.4 on 2024-12-24 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_course_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='order',
            field=models.PositiveIntegerField(default=1, verbose_name='Order'),
            preserve_default=False,
        ),
    ]