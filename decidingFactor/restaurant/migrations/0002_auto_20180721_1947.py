# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-07-21 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visithistory',
            name='last_visted',
            field=models.DateField(default=None, null=True),
        ),
    ]