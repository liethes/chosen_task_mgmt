# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectStaff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
            ],
            options={
                'verbose_name': '项目人员',
                'verbose_name_plural': '项目人员',
            },
        ),
        migrations.AlterModelOptions(
            name='mpttfood',
            options={'verbose_name': '食物（测试）', 'verbose_name_plural': '食物（测试）'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': '项目', 'verbose_name_plural': '项目'},
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'verbose_name': '人员', 'verbose_name_plural': '人员'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': '任务', 'verbose_name_plural': '任务'},
        ),
        migrations.AlterField(
            model_name='task',
            name='sender',
            field=models.ForeignKey(related_name='sender', to='tasks.Staff', verbose_name='发出人', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='projectstaff',
            name='projectId',
            field=models.ForeignKey(to='tasks.Project', verbose_name='人员ID', default=0),
        ),
        migrations.AddField(
            model_name='projectstaff',
            name='staffId',
            field=models.ForeignKey(to='tasks.Staff', verbose_name='人员ID', default=0),
        ),
    ]
