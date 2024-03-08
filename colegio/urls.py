from django.contrib import admin
from django.urls import path
from gestion import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.mostrarIndex),
    path('login', views.iniciarSesion),
    path('logout', views.cerrarSesion),

    path('menuadmin/', views.mostrarMenuAdmin),


    path('funcionarios/', views.mostrarFuncionarios),
    path('registrar_funcionarios/', views.registrarFuncionarios),
    path('form_actualizar_funcionario/<int:id>', views.mostrarFormActualizarFuncionario),
    path('actualizar_funcionario/<int:id>', views.actualizarFuncionario, name='actualizar_funcionario'),
    path('eliminar_funcionario/<int:id>', views.eliminarFuncionario),
    path('filtroEmpieza/', views.filtroEmpieza),
    path('filtroContenga/', views.filtroContenga),
    path('filtroTermina/', views.filtroTermina),
    path('filtroOrden/', views.filtroOrden),

    #MATRICULA
    path('matricula/', views.mostrarMatricula),
    path('registrar_matricula/', views.registrarMatricula),
    path('actualizar_matricula/<int:id>', views.actualizarMatricula),
    path('form_actualizar_matricula/<int:id>', views.mostrarFormActualizarMatricula),
    path('eliminar_matricula/<int:id>', views.eliminarMatricula),
    path('filtroEmpiezaMatricula/', views.filtroEmpiezaMatricula),
    path('filtroContengaMatricula/', views.filtroContengaMatricula),
    path('filtroTerminaMatricula/', views.filtroTerminaMatricula),
    path('filtroOrdenMatricula/', views.filtroOrdenMatricula),

    #CURSOS
    path('cursos/', views.mostrarCursos),
    path('registrar_cursos/', views.registrarCursos),
    path('eliminar_curso/<int:id>/', views.eliminarCurso),
    path('form_actualizar_curso/<int:id>', views.mostrarFormActualizarCurso),
    path('actualizar_curso/<int:id>', views.actualizarCurso, name='actualizar_curso'),

    #CARGOS
    path('cargos/', views.mostrarCargos),
    path('registrar_cargo/', views.registrarCargo),
    path('eliminar_cargo/<int:id>', views.eliminarCargo),
    path('form_actualizar_cargo/<int:id>', views.mostrarFormActualizarCargo),
    path('actualizar_cargo/<int:id>', views.actualizarCargo, name='actualizar_cargo'),

    #ASIGNATURA
    path('asignaturas/', views.mostrarAsignaturas),
    path('crear_asignatura/', views.crearAsignatura),
    path('form_actualizar_asignatura/<int:id>', views.mostrarFormActualizarAsignatura),
    path('actualizar_asignatura/<int:id>', views.actualizarAsignatura, name='actualizar_asignatura'),
    path('eliminar_asignatura/<int:id>', views.eliminarAsignatura),



    #NACIONALIDADES
    path('registrar_nacionalidades/', views.registrarNacionalidades),
    path('form_actualizar_nacionalidad/<int:id>', views.mostrarFormActualizarNacionalidad),
    path('actualizar_nacionalidad/<int:id>', views.actualizarNacionalidad, name='actualizar_nacionalidad'),
    path('eliminar_nacionalidad/<int:id>', views.eliminarNacionalidad),
    path('nacionalidades/', views.mostrarNacionalidades),

    path('perfil/', views.mostrarPerfil),    
    path('menudocente/', views.mostrarMenuDocente),
    path('cambiarclave/<int:id>', views.mostrarCambiarClave),
    path('actualizar_clave/<int:id>', views.actualizarClave),

    path('perfil_docente/', views.mostrarPerfilDocente),
    path('cursos_docente/', views.mostrarCursoDocente),
    path('jefatura/', views.mostrarJefaturas),    
    path('historial/', views.mostrarHistorial)



]
