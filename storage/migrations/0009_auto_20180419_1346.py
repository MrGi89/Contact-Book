# Generated by Django 2.0.2 on 2018-04-19 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0008_auto_20180417_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=64, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='address',
            name='flat_number',
            field=models.SmallIntegerField(null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='address',
            name='house_number',
            field=models.SmallIntegerField(verbose_name=''),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(max_length=64, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='email',
            name='address',
            field=models.EmailField(blank=True, max_length=64, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='email',
            name='email_type',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'Personal'), (2, 'Business'), (3, 'Other')], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='person',
            name='description',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='phone',
            name='number',
            field=models.BigIntegerField(blank=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='phone',
            name='number_type',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'Home'), (2, 'Business'), (3, 'Mobile'), (4, 'Other')], verbose_name=''),
        ),
    ]
