# Generated by Django 2.1 on 2018-09-10 16:12

from django.db import migrations, models
import registration.models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0014_auto_20180910_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veterinaria',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=registration.models.custom_upload_to_v),
        ),
    ]
