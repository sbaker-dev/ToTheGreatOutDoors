# Generated by Django 3.2.15 on 2022-09-07 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_comment_comment_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_group',
            field=models.IntegerField(default=0),
        ),
    ]
