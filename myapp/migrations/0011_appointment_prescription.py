# Generated by Django 4.0.5 on 2022-07-26 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_helthprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='prescription',
            field=models.TextField(default='not given yet'),
        ),
    ]
