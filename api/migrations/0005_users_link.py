# Generated by Django 3.2 on 2024-03-31 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20240331_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
