# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencebook',
            name='number',
            field=models.CharField(max_length=10, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0432 \u0441\u0435\u0440\u0438\u0438', blank=True),
            preserve_default=True,
        ),
    ]
