# Generated by Django 3.0 on 2020-11-09 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webphishingClient', '0014_auto_20201109_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colaboratorcampaign',
            name='clicked_extradata',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='colaboratorcampaign',
            name='compromised_extradata',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='colaboratorcampaign',
            name='opened_extradata',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='colaboratorcampaign',
            name='sent_extradata',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
