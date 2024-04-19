# Generated by Django 5.0.4 on 2024-04-19 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0004_alter_sleep_station'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='station',
            name='localtime',
        ),
        migrations.RemoveField(
            model_name='station',
            name='localtime_epoch',
        ),
        migrations.RemoveField(
            model_name='weatherapi',
            name='condition_code',
        ),
        migrations.RemoveField(
            model_name='weatherapi',
            name='condition_icon',
        ),
        migrations.RemoveField(
            model_name='weatherapi',
            name='is_day',
        ),
        migrations.RemoveField(
            model_name='weatherapi',
            name='last_updated',
        ),
        migrations.RemoveField(
            model_name='weatherapi',
            name='last_updated_epoch',
        ),
        migrations.RemoveField(
            model_name='weatherapi',
            name='precip_in',
        ),
        migrations.RemoveField(
            model_name='weatherapi',
            name='temp_f',
        ),
    ]