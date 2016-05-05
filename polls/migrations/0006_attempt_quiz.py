# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_quizattempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='polls.Quiz', null=True),
        ),
    ]
