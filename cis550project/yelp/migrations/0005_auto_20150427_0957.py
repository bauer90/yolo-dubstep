# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yelp', '0004_userprofile_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(default=b'WI', max_length=2),
        ),
    ]
