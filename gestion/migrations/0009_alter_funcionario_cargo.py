# Generated by Django 4.2.7 on 2023-11-22 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0008_alter_funcionario_cargo_alter_funcionario_correo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='cargo',
            field=models.TextField(max_length=100),
        ),
    ]