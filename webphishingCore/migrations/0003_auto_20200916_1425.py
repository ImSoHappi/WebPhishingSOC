# Generated by Django 3.1.1 on 2020-09-16 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webphishingCore', '0002_auto_20200916_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignmodel',
            name='body',
            field=models.TextField(default='none'),
        ),
        migrations.AddField(
            model_name='campaignmodel',
            name='subject',
            field=models.CharField(default='none', max_length=100),
        ),
    ]
