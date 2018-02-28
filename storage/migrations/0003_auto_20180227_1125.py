# Generated by Django 2.0.2 on 2018-02-27 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_auto_20180226_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='email_type',
            field=models.SmallIntegerField(choices=[(1, 'Home phone'), (2, 'Business phone'), (3, 'Mobile phone'), (4, 'Other')]),
        ),
        migrations.AlterField(
            model_name='phone',
            name='number_type',
            field=models.SmallIntegerField(choices=[(1, 'Home phone'), (2, 'Business phone'), (3, 'Mobile phone'), (4, 'Other')]),
        ),
    ]