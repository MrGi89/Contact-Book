# Generated by Django 2.0.2 on 2018-02-26 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=64)),
                ('street', models.CharField(max_length=64)),
                ('house_number', models.SmallIntegerField()),
                ('flat_number', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=64)),
                ('email_type', models.CharField(choices=[(1, 'home phone'), (2, 'business phone'), (3, 'mobile phone'), (4, 'other')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.SmallIntegerField()),
                ('number_type', models.CharField(choices=[(1, 'home phone'), (2, 'business phone'), (3, 'mobile phone'), (4, 'other')], max_length=30)),
                ('person_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numbers', to='storage.Person')),
            ],
        ),
        migrations.AddField(
            model_name='email',
            name='person_email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='storage.Person'),
        ),
        migrations.AddField(
            model_name='address',
            name='person_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='storage.Person'),
        ),
    ]
