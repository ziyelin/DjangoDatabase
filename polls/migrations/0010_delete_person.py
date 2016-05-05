# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_remove_attempt_person'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Person',
        ),
    ]
