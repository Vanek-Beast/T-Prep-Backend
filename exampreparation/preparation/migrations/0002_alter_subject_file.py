# Generated by Django 5.1.2 on 2024-11-02 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preparation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='questions',
            field=models.JSONField(),
        ),
    ]
