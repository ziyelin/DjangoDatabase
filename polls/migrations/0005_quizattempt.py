# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_attempt_finish_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.DecimalField(default=0.0, max_digits=5, decimal_places=2)),
                ('attempt', models.ForeignKey(to='polls.Attempt')),
                ('quiz', models.ForeignKey(to='polls.Quiz')),
            ],
        ),
    ]
