# Generated by Django 3.2.15 on 2022-08-11 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220810_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boundary',
            name='place',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='location',
            name='place',
            field=models.TextField(),
        ),
        migrations.DeleteModel(
            name='Place',
        ),
    ]
