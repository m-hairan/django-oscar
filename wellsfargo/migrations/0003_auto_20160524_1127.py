# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-24 11:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wellsfargo', '0002_auto_20160523_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='cacreditapp',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credit_applications', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),  # NOQA
        ),
        migrations.AddField(
            model_name='cajointcreditapp',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credit_applications', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),  # NOQA
        ),
        migrations.AddField(
            model_name='uscreditapp',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credit_applications', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),  # NOQA
        ),
        migrations.AddField(
            model_name='usjointcreditapp',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credit_applications', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),  # NOQA
        ),
    ]