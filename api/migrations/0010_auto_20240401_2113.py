# Generated by Django 3.2 on 2024-04-01 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20240401_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batch',
            name='supplier',
        ),
        migrations.AddField(
            model_name='batch',
            name='supplierId',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.supplier'),
        ),
    ]
