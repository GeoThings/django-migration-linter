# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 14:06
from __future__ import unicode_literals

from django.db import migrations, models

from test_app import migrations_utils

class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_create_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='a',
            name='new_not_null_field',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations_utils.AddDefaultValue(
            model_name='a',
            name='new_not_null_field',
            value='1',
        )
    ]
