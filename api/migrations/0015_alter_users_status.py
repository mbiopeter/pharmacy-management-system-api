# Generated by Django 3.2 on 2024-04-03 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_users_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='status',
            field=models.CharField(blank=True, default='Active', max_length=200, null=True),
        ),
    ]
