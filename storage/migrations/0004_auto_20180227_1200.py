# Generated by Django 2.0.2 on 2018-02-27 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_auto_20180227_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='number',
            field=models.IntegerField(),
        ),
    ]
