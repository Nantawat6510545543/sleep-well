# Generated by Django 5.0.4 on 2024-04-27 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0011_rename_sleep_comments_sleep_sleep_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sleep',
            name='sleep_duration',
            field=models.FloatField(),
        ),
    ]
