# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject_id', models.PositiveIntegerField()),
                ('experiencer', models.CharField(default=b'Anonymous', max_length=64)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('subject_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.DecimalField(max_digits=5, decimal_places=2)),
                ('metric', models.CharField(default=b'overall', max_length=64)),
                ('experience', models.ForeignKey(to='experiences.Experience')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approved', models.BooleanField(default=False)),
                ('text', models.TextField()),
                ('experience', models.ForeignKey(to='experiences.Experience')),
            ],
        ),
    ]
