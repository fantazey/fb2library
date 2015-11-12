# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(default=b'000', max_length=200, verbose_name='\u0418\u043c\u044f')),
                ('middle_name', models.CharField(max_length=200, null=True, verbose_name='\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e', blank=True)),
                ('last_name', models.CharField(default=b'000', max_length=200, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f')),
            ],
            options={
                'verbose_name': '\u0410\u0432\u0442\u043e\u0440',
                'verbose_name_plural': '\u0410\u0432\u0442\u043e\u0440\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('annotation', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('date', models.CharField(max_length=50, null=True, verbose_name='\u0414\u0430\u0442\u0430', blank=True)),
                ('book_file', models.CharField(max_length=1000, verbose_name='\u0424\u0430\u0439\u043b')),
                ('image', models.ImageField(max_length=300, upload_to=b'covers/', null=True, verbose_name='\u041e\u0431\u043b\u043e\u0436\u043a\u0430', blank=True)),
                ('md5', models.CharField(default=b'000', max_length=150, verbose_name='Hash')),
                ('uuid', models.CharField(max_length=30, null=True, verbose_name='UUID', blank=True)),
            ],
            options={
                'verbose_name': '\u041a\u043d\u0438\u0433\u0430',
                'verbose_name_plural': '\u041a\u043d\u0438\u0433\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=50, verbose_name='\u041a\u043e\u0434 \u0436\u0430\u043d\u0440\u0430')),
                ('name', models.CharField(max_length=300, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0436\u0430\u043d\u0440\u0430', blank=True)),
            ],
            options={
                'verbose_name': '\u0416\u0430\u043d\u0440',
                'verbose_name_plural': '\u0416\u0430\u043d\u0440\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=50, verbose_name='\u041a\u043e\u0434 \u044f\u0437\u044b\u043a\u0430')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u042f\u0437\u044b\u043a',
                'verbose_name_plural': '\u042f\u0437\u044b\u043a\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0438\u0437\u0434\u0430\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u0430')),
                ('city', models.CharField(max_length=100, null=True, verbose_name='\u0413\u043e\u0440\u043e\u0434', blank=True)),
                ('website', models.URLField(null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441 \u0441\u0430\u0439\u0442\u0430', blank=True)),
                ('year', models.CharField(max_length=20, null=True, verbose_name='\u0413\u043e\u0434', blank=True)),
            ],
            options={
                'verbose_name': '\u0418\u0437\u0434\u0430\u0442\u0435\u043b\u044c',
                'verbose_name_plural': '\u0418\u0437\u0434\u0430\u0442\u0435\u043b\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u0435\u0440\u0438\u0438')),
            ],
            options={
                'verbose_name': '\u0421\u0435\u0440\u0438\u044f',
                'verbose_name_plural': '\u0421\u0435\u0440\u0438\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SequenceBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.FloatField(null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0432 \u0441\u0435\u0440\u0438\u0438', blank=True)),
                ('book', models.ForeignKey(verbose_name='\u041a\u043d\u0438\u0433\u0430', blank=True, to='book.Book', null=True)),
                ('sequence', models.ForeignKey(verbose_name='\u0416\u0430\u043d\u0440', blank=True, to='book.Sequence', null=True)),
            ],
            options={
                'verbose_name': '\u0421\u0435\u0440\u0438\u044f \u043a\u043d\u0438\u0433\u0438',
                'verbose_name_plural': '\u0421\u0435\u0440\u0438\u0438 \u043a\u043d\u0438\u0433',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Translator',
            fields=[
                ('author_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='book.Author')),
            ],
            options={
                'verbose_name': '\u041f\u0435\u0440\u0435\u0432\u043e\u0434\u0447\u0438\u043a',
                'verbose_name_plural': '\u041f\u0435\u0440\u0435\u0432\u043e\u0434\u0447\u0438\u043a\u0438',
            },
            bases=('book.author',),
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(related_name='authors', verbose_name='\u0410\u0432\u0442\u043e\u0440\u044b', to='book.Author'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(to='book.Genre', null=True, verbose_name='\u0416\u0430\u043d\u0440\u044b'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='lang',
            field=models.ForeignKey(related_name='book_lang', verbose_name='\u042f\u0437\u044b\u043a', to='book.Language', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ManyToManyField(to='book.Publisher', null=True, verbose_name='\u0418\u0437\u0434\u0430\u0442\u0435\u043b\u044c'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='sequence',
            field=models.ManyToManyField(to='book.Sequence', null=True, verbose_name='\u0421\u0435\u0440\u0438\u0438 \u043a\u043d\u0438\u0433\u0438', through='book.SequenceBook'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='src_lang',
            field=models.ForeignKey(related_name='book_src_lang', verbose_name='\u042f\u0437\u044b\u043a \u043e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u0430', to='book.Language', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='translator',
            field=models.ManyToManyField(related_name='translators', null=True, verbose_name='\u041f\u0435\u0440\u0435\u0432\u043e\u0434\u0447\u0438\u043a', to='book.Translator'),
            preserve_default=True,
        ),
    ]
