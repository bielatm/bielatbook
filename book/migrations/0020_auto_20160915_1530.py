# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0019_membership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(related_name='user_memberships', to=settings.AUTH_USER_MODEL),
        ),
    ]
