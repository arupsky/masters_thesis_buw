# Generated by Django 4.0.1 on 2022-06-02 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pupils', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diameterinfo',
            name='distance',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
