# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20170219_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rh_token',
            field=models.CharField(max_length=255, null=True),
        ),
    ]