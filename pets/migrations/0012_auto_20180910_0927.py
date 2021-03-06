# Generated by Django 2.1 on 2018-09-10 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0014_auto_20180910_0131'),
        ('pets', '0011_auto_20180910_0136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Camara',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('veterinaria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='get_camaras', to='registration.Veterinaria')),
            ],
        ),
        migrations.AlterField(
            model_name='servicios',
            name='cliente',
            field=models.PositiveIntegerField(verbose_name='Cc dueño'),
        ),
    ]
