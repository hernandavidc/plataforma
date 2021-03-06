# Generated by Django 2.1 on 2018-10-11 07:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0013_auto_20180910_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnotacionMascota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=400, verbose_name='anotacion')),
            ],
            options={
                'verbose_name': 'Anotacion mascota',
                'verbose_name_plural': 'Anotaciones mascotas',
                'ordering': ['-id'],
            },
        ),
        migrations.AlterField(
            model_name='mascota',
            name='dueno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='get_pets', to=settings.AUTH_USER_MODEL, verbose_name='Dueño'),
        ),
        migrations.AddField(
            model_name='anotacionmascota',
            name='mascota',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pets.Mascota', verbose_name='Mascota'),
        ),
    ]
