# Generated by Django 4.1.4 on 2022-12-21 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_corn_grain_yield_corngrainyield_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weather',
            old_name='max_temp',
            new_name='maximum_temperature',
        ),
        migrations.RenameField(
            model_name='weather',
            old_name='min_temp',
            new_name='minimum_temperature',
        ),
        migrations.RenameField(
            model_name='weatheranalysis',
            old_name='max_temp_avg',
            new_name='maximum_temperature_average',
        ),
        migrations.RenameField(
            model_name='weatheranalysis',
            old_name='min_temp_avg',
            new_name='minimum_temperature_average',
        ),
    ]
