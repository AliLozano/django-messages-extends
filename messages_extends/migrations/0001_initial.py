# -*- coding: utf-8 -*-
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('level', models.IntegerField(choices=[(11, 'PERSISTENT DEBUG'), (21, 'PERSISTENT INFO'), (26, 'PERSISTENT SUCCESS'), (31, 'PERSISTENT WARNING'), (41, 'PERSISTENT ERROR')])),
                ('extra_tags', models.CharField(max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('read', models.BooleanField(default=False)),
                ('expires', models.DateTimeField(null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
            ],
        ),
    ]
