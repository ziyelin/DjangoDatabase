# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(default=b'a description of the answer', blank=True)),
                ('score', models.DecimalField(default=1.0, max_digits=2, decimal_places=1)),
            ],
        ),
        migrations.CreateModel(
            name='AnswerAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.ForeignKey(to='polls.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_score', models.DecimalField(default=0.0, max_digits=5, decimal_places=2)),
                ('answer', models.ManyToManyField(to='polls.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=40)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('text', models.TextField(default=b'a description of the question', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'title of the quiz', max_length=60, blank=True)),
                ('description', models.TextField(default=b'a description of the quiz', blank=True)),
                ('question_total_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(default=1, to='polls.Quiz'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='person',
            field=models.ForeignKey(to='polls.Person'),
        ),
        migrations.AddField(
            model_name='answerattempt',
            name='attempt',
            field=models.ForeignKey(to='polls.Attempt'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=1, blank=True, to='polls.Question'),
        ),
    ]
