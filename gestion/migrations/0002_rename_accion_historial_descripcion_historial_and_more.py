# Generated by Django 4.2.7 on 2023-11-16 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historial',
            old_name='accion',
            new_name='descripcion_historial',
        ),
        migrations.RenameField(
            model_name='historial',
            old_name='fecha_hora',
            new_name='fecha_hora_historial',
        ),
    ]
