# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-06-23 04:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='restaurant_type',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='visithistory',
            name='rating',
            field=models.CharField(choices=[('undecided', 'Undecided'), ('hate', 'Hated'), ('like', 'Liked'), ('love', 'Loved')], default='undecided', max_length=10),
        ),
    ]