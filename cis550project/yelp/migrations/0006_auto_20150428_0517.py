# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yelp', '0005_auto_20150427_0957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='picture',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='desired_1',
            field=models.CharField(default=b'000000000000', max_length=22),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='desired_2',
            field=models.CharField(default=b'000000000000', max_length=22),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='desired_3',
            field=models.CharField(default=b'000000000000', max_length=22),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='preference',
            field=models.CharField(default=b'Restaurants', max_length=20),
        ),
    ]
