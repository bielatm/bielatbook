# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_friendshipinvite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendshipinvite',
            name='friend',
            field=models.ForeignKey(related_name='received_friendship_invites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendshipinvite',
            name='user',
            field=models.ForeignKey(related_name='sent_friendship_invites', to=settings.AUTH_USER_MODEL),
        ),
    ]
