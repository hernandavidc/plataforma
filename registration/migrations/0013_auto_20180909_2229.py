# Generated by Django 2.1 on 2018-09-10 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_auto_20180909_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veterinaria',
            name='rut',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='RUT'),
        ),
    ]