# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20151018_0321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectstaff',
            old_name='projectId',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='projectstaff',
            old_name='staffId',
            new_name='staff',
        ),
        migrations.AlterField(
            model_name='staff',
            name='email',
            field=models.CharField(verbose_name='电邮', null=True, max_length=250),
        ),
    ]
