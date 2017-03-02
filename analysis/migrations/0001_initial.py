# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-23 10:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stars', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
                ('note', models.TextField(default='')),
                ('reference', models.TextField(default='')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
                ('description', models.TextField(default='')),
                ('slug', models.SlugField(default='', max_length=10, unique=True)),
                ('color', models.CharField(default='#8B0000', max_length=7)),
                ('data_type', models.CharField(choices=[('gen', 'Generic'), ('sed', 'SED hdf5')], default='gen', max_length=7)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('component', models.IntegerField(choices=[(0, 'System'), (1, 'Primary'), (2, 'Secondary'), (5, 'Circumbinary Disk')], default=0)),
                ('value', models.FloatField()),
                ('error_l', models.FloatField(default=0.0)),
                ('error_u', models.FloatField(default=0.0)),
                ('valid', models.BooleanField(default=True)),
                ('unit', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('datasource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='analysis.DataSource')),
                ('datafile', models.FileField(upload_to='datasets/')),
                ('valid', models.BooleanField(default=True)),
                ('method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='analysis.Method')),
                ('star', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stars.Star')),
            ],
            bases=('analysis.datasource',),
        ),
        migrations.CreateModel(
            name='DataTable',
            fields=[
                ('datasource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='analysis.DataSource')),
                ('datafile', models.FileField(upload_to='datatables/')),
                ('columnnames', models.TextField(default='')),
                ('xdim', models.IntegerField(default=0)),
                ('ydim', models.IntegerField(default=0)),
            ],
            bases=('analysis.datasource',),
        ),
        migrations.AddField(
            model_name='parameter',
            name='data_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='analysis.DataSource'),
        ),
        migrations.AddField(
            model_name='parameter',
            name='star',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stars.Star'),
        ),
    ]
