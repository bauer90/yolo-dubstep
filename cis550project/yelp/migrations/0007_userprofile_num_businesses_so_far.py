# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yelp', '0006_auto_20150428_0517'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='num_businesses_so_far',
            field=models.IntegerField(default=0),
        ),
    ]
