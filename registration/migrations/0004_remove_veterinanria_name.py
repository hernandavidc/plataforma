# Generated by Django 2.1 on 2018-08-06 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20180804_1913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='veterinanria',
            name='name',
        ),
    ]
