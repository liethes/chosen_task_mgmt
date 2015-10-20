# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20151020_1013'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imgUrl', models.CharField(max_length=500)),
                ('task', models.ForeignKey(verbose_name='任务图片', to='tasks.Task')),
            ],
        ),
    ]
