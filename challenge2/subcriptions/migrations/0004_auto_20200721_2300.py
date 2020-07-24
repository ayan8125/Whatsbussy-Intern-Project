# Generated by Django 2.2.5 on 2020-07-21 17:30

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('subcriptions', '0003_auto_20200721_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='current_period_start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='current_end_At',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 20, 17, 30, 11, 318166, tzinfo=utc)),
        ),
    ]