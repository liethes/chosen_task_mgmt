# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20151018_0300'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='desc',
            field=models.CharField(null=True, verbose_name='描述', max_length=250),
        ),
        migrations.AlterField(
            model_name='projectstaff',
            name='projectId',
            field=models.ForeignKey(to='tasks.Project', verbose_name='项目', default=0),
        ),
        migrations.AlterField(
            model_name='projectstaff',
            name='staffId',
            field=models.ForeignKey(to='tasks.Staff', verbose_name='人员', default=0),
        ),
        migrations.AlterField(
            model_name='staff',
            name='email',
            field=models.CharField(verbose_name='电邮', max_length=250),
        ),
    ]
