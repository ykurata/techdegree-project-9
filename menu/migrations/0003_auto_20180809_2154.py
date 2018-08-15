# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20160406_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='chef',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='chef'),
        ),
        migrations.AlterField(
            model_name='item',
            name='ingredients',
            field=models.ManyToManyField(to='menu.Ingredient', related_name='ingredients'),
        ),
    ]
