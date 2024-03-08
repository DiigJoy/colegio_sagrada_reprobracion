# Generated by Django 4.2.4 on 2023-11-29 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0010_alter_funcionario_correo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matricula',
            old_name='cursos',
            new_name='curso',
        ),
        migrations.RemoveField(
            model_name='funcionario',
            name='asignaturas',
        ),
        migrations.RemoveField(
            model_name='funcionario',
            name='cursos',
        ),
        migrations.RemoveField(
            model_name='funcionario',
            name='jefatura_cursos',
        ),
        migrations.RemoveField(
            model_name='matricula',
            name='apoderado_nacionalidades',
        ),
        migrations.RemoveField(
            model_name='matricula',
            name='estudiante_nacionalidades',
        ),
        migrations.AddField(
            model_name='funcionario',
            name='asignatura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion.asignatura'),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='curso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion.curso'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='apoderado_nacionalidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matriculas_apoderados', to='gestion.nacionalidad'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='estudiante_nacionalidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matriculas_estudiantes', to='gestion.nacionalidad'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='cargo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.cargo'),
        ),
    ]
