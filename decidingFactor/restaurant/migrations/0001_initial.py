# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-09 03:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('last_dining', models.DateField()),
                ('times_gone', models.IntegerField()),
                ('liked', models.BooleanField()),
                ('hated', models.BooleanField()),
                ('trying', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_code', models.IntegerField()),
                ('search_term', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='zip_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Search'),
        ),
    ]
