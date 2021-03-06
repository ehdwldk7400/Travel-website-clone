# Generated by Django 3.0.3 on 2020-03-28 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='agree_location',
        ),
        migrations.RemoveField(
            model_name='account',
            name='agree_promotion',
        ),
        migrations.RemoveField(
            model_name='account',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='account',
            name='social_id',
        ),
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='password',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
