# Generated by Django 5.0.4 on 2024-04-19 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0005_remove_station_localtime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='sex',
            field=models.CharField(max_length=10),
        ),
    ]
