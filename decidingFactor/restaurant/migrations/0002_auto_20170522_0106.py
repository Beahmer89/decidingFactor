# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-22 01:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='loved',
            field=models.BooleanField(default=b'False'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='search',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='restaurant.Search'),
        ),
        migrations.AddField(
            model_name='search',
            name='city',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='search',
            name='search_name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='search',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='hated',
            field=models.BooleanField(default=b'False'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='last_dining',
            field=models.DateField(default=b'null'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='liked',
            field=models.BooleanField(default=b'False'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='times_gone',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='trying',
            field=models.BooleanField(verbose_name=b'False'),
        ),
        migrations.AlterField(
            model_name='search',
            name='search_term',
            field=models.CharField(default=None, max_length=30),
        ),
        migrations.AlterField(
            model_name='search',
            name='zip_code',
            field=models.IntegerField(default=0),
        ),
    ]