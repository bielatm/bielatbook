# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0012_message_date_of_sending_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='date_of_sending_message',
            new_name='created_at',
        ),
    ]
