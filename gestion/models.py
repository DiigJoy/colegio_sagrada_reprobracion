from django.db import models


class Usuario(models.Model):
    nombre_usuario = models.TextField(max_length=15)
    password_usuario = models.TextField(max_length=20)


class Curso(models.Model):
    nombre_curso = models.TextField(max_length=100)


class Nacionalidad(models.Model):
    nombre_nacionalidad = models.TextField(max_length=100)


class Asignatura(models.Model):
    nombre_asignatura = models.TextField(max_length=100)


class Cargo(models.Model):
    nombre_cargo = models.TextField(max_length=100)

class Funcionario(models.Model):
    rut = models.TextField(max_length=20)
    nombres = models.TextField(max_length=100)
    paterno = models.TextField(max_length=100)
    materno = models.TextField(max_length=100)
    correo = models.EmailField(max_length=100)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, related_name='curso', on_delete=models.CASCADE, null=True, blank=True)
    jefatura = models.ForeignKey(Curso, related_name='jefatura', on_delete=models.CASCADE, null=True, blank=True)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, null=True, blank=True)


class Matricula(models.Model):
    apoderado_rut = models.TextField(max_length=20)
    apoderado_nombres = models.TextField(max_length=100)
    apoderado_paterno = models.TextField(max_length=100)
    apoderado_materno = models.TextField(max_length=100)
    apoderado_edad = models.PositiveIntegerField()
    apoderado_parentesco = models.TextField(max_length=100)
    apoderado_nacionalidad = models.ForeignKey(Nacionalidad, related_name='matriculas_apoderados', on_delete=models.CASCADE, null=True, blank=True)
    estudiante_rut = models.TextField(max_length=20)
    estudiante_nombres = models.TextField(max_length=100)
    estudiante_paterno = models.TextField(max_length=100)
    estudiante_materno = models.TextField(max_length=100)
    estudiante_edad = models.PositiveIntegerField()
    estudiante_nacionalidad = models.ForeignKey(Nacionalidad, related_name='matriculas_estudiantes', on_delete=models.CASCADE, null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

class Historial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion_historial = models.TextField(max_length=200)
    tabla_afectada_historial = models.TextField(max_length=100)
    fecha_hora_historial = models.DateTimeField()


