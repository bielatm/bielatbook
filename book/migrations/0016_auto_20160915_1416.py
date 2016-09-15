# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0015_group_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='admin',
            field=models.ForeignKey(related_name='user_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]
