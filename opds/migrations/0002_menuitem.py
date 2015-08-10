# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opds', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300, null=True, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a', blank=True)),
                ('link', models.CharField(max_length=400, null=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430', blank=True)),
                ('description', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('group', models.CharField(max_length=40, null=True, verbose_name='\u0413\u0440\u0443\u043f\u043f\u0430', blank=True)),
                ('order', models.IntegerField(default=0, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
