# Generated by Django 5.1.4 on 2025-01-11 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0004_remove_usertest_submitted_at_usetask'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertest',
            name='user_lesson',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_tests', to='progress.userlesson', verbose_name='Қолданушының сабағы'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usetask',
            name='submission',
            field=models.FileField(upload_to='main/subject/user/tasks/', verbose_name='Тапсырма'),
        ),
    ]
