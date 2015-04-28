# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yelp', '0007_userprofile_num_businesses_so_far'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='desired_1',
            field=models.CharField(default=b'', max_length=22),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='desired_2',
            field=models.CharField(default=b'', max_length=22),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='desired_3',
            field=models.CharField(default=b'', max_length=22),
        ),
    ]
