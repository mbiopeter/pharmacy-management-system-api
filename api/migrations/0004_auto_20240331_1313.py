# Generated by Django 3.2 on 2024-03-31 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='contact',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
