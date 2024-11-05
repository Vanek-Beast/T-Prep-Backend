# Generated by Django 5.1.2 on 2024-11-01 16:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('user_password', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('time', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('questions', models.FileField(upload_to='upldfile/')),
                # ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='preparation.user')),
                ('user_id', models.IntegerField())
            ],
        ),
    ]
