# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-23 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gradnet', '0003_auto_20170123_0653'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=800)),
                ('answer', models.CharField(max_length=800)),
                ('publish', models.BooleanField(default=False)),
            ],
        ),
    ]