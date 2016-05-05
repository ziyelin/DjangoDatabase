# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20160328_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='finish_status',
            field=models.BooleanField(default=False),
        ),
    ]
