# Generated by Django 3.1.1 on 2020-09-21 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webphishingApi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fishinghookmodel',
            name='name',
            field=models.CharField(default='hola', max_length=50),
        ),
    ]
