# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MPTTFood',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=50)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', models.ForeignKey(null=True, related_name='childrem', blank=True, to='tasks.MPTTFood')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='项目名称', max_length=100)),
                ('desc', models.TextField(verbose_name='详细描述', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='姓名', max_length=50)),
                ('email', models.CharField(verbose_name='详细描述', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='任务名称', max_length=100)),
                ('type', models.CharField(choices=[('CAM', '镜头类'), ('MAT', '素材类')], verbose_name='任务类型', max_length=4)),
                ('desc', models.TextField(verbose_name='详细描述', null=True)),
                ('bgn_date', models.DateField(verbose_name='开始日期')),
                ('end_date', models.DateField(verbose_name='结束日期')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('owner', models.ForeignKey(verbose_name='制作人', null=True, related_name='owner', blank=True, to='tasks.Staff')),
                ('parent_task', models.ForeignKey(verbose_name='父任务', null=True, blank=True, to='tasks.Task')),
                ('project', models.ForeignKey(verbose_name='所属项目', default=0, to='tasks.Project')),
                ('sender', models.ForeignKey(verbose_name='制作人', null=True, related_name='sender', blank=True, to='tasks.Staff')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
