# Generated by Django 2.1 on 2018-08-21 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0003_auto_20180816_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='mascota',
            name='tipo',
            field=models.CharField(choices=[('c', 'Gato'), ('d', 'Perro'), ('f', 'Pez'), ('b', 'Ave'), ('r', 'Reptil'), ('o', 'Otro')], default='d', max_length=1),
            preserve_default=False,
        ),
    ]
