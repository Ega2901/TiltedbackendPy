# Generated by Django 5.0.7 on 2024-08-02 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_globaltask_task_url_alter_usertaskstatus_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, to='main.user'),
        ),
    ]
