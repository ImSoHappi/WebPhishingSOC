# Generated by Django 3.1.1 on 2020-09-14 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='campaignModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='clientModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('disabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='csvModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csvfile', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='exerciseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('campaigns', models.ManyToManyField(blank=True, to='webphishingCore.campaignModel')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webphishingCore.clientmodel')),
            ],
        ),
        migrations.CreateModel(
            name='employeesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('company', models.CharField(max_length=100)),
                ('data', models.TextField()),
                ('received', models.BooleanField(default=False)),
                ('read', models.BooleanField(default=False)),
                ('click', models.BooleanField(default=False)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webphishingCore.exercisemodel')),
            ],
        ),
    ]
