# Generated by Django 3.2.15 on 2022-09-07 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20220823_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='replies',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.comment'),
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
    ]
