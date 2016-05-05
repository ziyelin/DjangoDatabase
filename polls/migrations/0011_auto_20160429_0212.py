# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_delete_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(default=b'a description of the answer, must be filled', blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(default=b'a description of the question, must be filled', blank=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=models.TextField(default=b'a description of the quiz,can be blank', blank=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(default=b'title of the quiz,must be filled', max_length=60, blank=True),
        ),
    ]
