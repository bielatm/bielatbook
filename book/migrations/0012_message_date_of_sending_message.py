# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date_of_sending_message',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
