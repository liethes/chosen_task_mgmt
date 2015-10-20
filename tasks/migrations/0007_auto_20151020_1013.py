# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_task_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Camper',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30)),
                ('img', models.FileField(upload_to='./upload')),
            ],
        ),
        migrations.RemoveField(
            model_name='mpttfood',
            name='parent',
        ),
        migrations.DeleteModel(
            name='MPTTFood',
        ),
    ]
