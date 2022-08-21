# Generated by Django 3.2.15 on 2022-08-18 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rastermap'),
    ]

    operations = [
        migrations.AddField(
            model_name='rastermap',
            name='size',
            field=models.FloatField(default=-1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rastermap',
            name='x',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='rastermap',
            name='y',
            field=models.FloatField(),
        ),
    ]
