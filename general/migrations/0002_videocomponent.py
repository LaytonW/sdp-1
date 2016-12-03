# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 11:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('content', models.URLField()),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Module')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]