# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_attempt_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
    ]
