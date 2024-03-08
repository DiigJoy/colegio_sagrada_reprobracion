from django.contrib import admin
from .models import Usuario, Curso, Nacionalidad, Asignatura, Funcionario, Matricula, Historial

admin.site.register(Usuario)
admin.site.register(Curso)
admin.site.register(Nacionalidad)
admin.site.register(Asignatura)
admin.site.register(Funcionario)
admin.site.register(Matricula)
admin.site.register(Historial)
