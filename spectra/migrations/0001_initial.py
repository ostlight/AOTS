# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-23 09:57
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
            name='SpecFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hjd', models.FloatField(default=0)),
                ('instrument', models.CharField(default='', max_length=200)),
                ('filetype', models.CharField(default='', max_length=200)),
                ('specfile', models.FileField(upload_to='spectra/')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Spectrum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hjd', models.FloatField(default=0)),
                ('ra', models.FloatField(default=0)),
                ('dec', models.FloatField(default=0)),
                ('alt', models.FloatField(default=0)),
                ('az', models.FloatField(default=0)),
                ('airmass', models.FloatField(default=0)),
                ('exptime', models.FloatField(default=0)),
                ('barycor', models.FloatField(default=0)),
                ('telescope', models.CharField(default='', max_length=200)),
                ('instrument', models.CharField(default='', max_length=200)),
                ('observer', models.CharField(default='', max_length=50)),
                ('moon_illumination', models.FloatField(default=0)),
                ('moon_separation', models.FloatField(default=0)),
                ('wind_speed', models.FloatField(default=0)),
                ('wind_direction', models.FloatField(default=0)),
                ('seeing', models.FloatField(default=0)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('star', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stars.Star')),
            ],
        ),
        migrations.AddField(
            model_name='specfile',
            name='spectrum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='spectra.Spectrum'),
        ),
    ]
