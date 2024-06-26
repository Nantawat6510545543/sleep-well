# Generated by Django 5.0.4 on 2024-04-21 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0009_noise_delete_noisestation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noise',
            name='country',
            field=models.CharField(default='Thailand', max_length=100),
        ),
        migrations.AlterField(
            model_name='noise',
            name='lat',
            field=models.FloatField(default=13.857139052152801),
        ),
        migrations.AlterField(
            model_name='noise',
            name='location_name',
            field=models.CharField(default='Nonthaburi', max_length=100),
        ),
        migrations.AlterField(
            model_name='noise',
            name='lon',
            field=models.FloatField(default=100.48867194387923),
        ),
        migrations.AlterField(
            model_name='noise',
            name='region',
            field=models.CharField(default='Nonthaburi', max_length=100),
        ),
        migrations.AlterField(
            model_name='noise',
            name='tz_id',
            field=models.CharField(default='Asia/Bangkok', max_length=50),
        ),
        migrations.AlterField(
            model_name='weather',
            name='country',
            field=models.CharField(default='Thailand', max_length=100),
        ),
        migrations.AlterField(
            model_name='weather',
            name='location_name',
            field=models.CharField(default='Nonthaburi', max_length=100),
        ),
        migrations.AlterField(
            model_name='weather',
            name='region',
            field=models.CharField(default='Nonthaburi', max_length=100),
        ),
        migrations.AlterField(
            model_name='weather',
            name='tz_id',
            field=models.CharField(default='Asia/Bangkok', max_length=50),
        ),
    ]
