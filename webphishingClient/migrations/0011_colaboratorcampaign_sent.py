# Generated by Django 3.0 on 2020-11-05 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webphishingClient', '0010_campaign_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaboratorcampaign',
            name='sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]