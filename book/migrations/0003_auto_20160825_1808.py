# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20160825_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_id',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
