# Generated by Django 3.0 on 2020-11-03 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webphishingClient', '0004_auto_20201102_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colaborator',
            name='extra_data',
            field=models.TextField(blank=True, default=''),
        ),
    ]