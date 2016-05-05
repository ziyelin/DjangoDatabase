# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_attempt_last_modified'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizQuestionAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quiz', models.CharField(default=b'title of the quiz', max_length=60, blank=True)),
                ('question', models.TextField(default=b'a description of the question', blank=True)),
                ('answer', models.TextField(default=b'a description of the answer', blank=True)),
                ('score', models.DecimalField(default=0.0, max_digits=5, decimal_places=2)),
            ],
        ),
    ]
