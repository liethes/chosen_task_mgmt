# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0004_auto_20151018_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.ForeignKey(verbose_name='对应用户', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
