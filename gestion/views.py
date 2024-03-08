from django.shortcuts import render, redirect
from django.http import HttpResponse
from gestion.models import Curso, Nacionalidad, Funcionario, Matricula, Asignatura, Historial, Usuario, Cargo
from datetime import datetime

# Create your views here.

def mostrarIndex(request):
    return render(request, "index.html")

#------------------------------------------------------------------------------------------------------------------------------------

def iniciarSesion(request):
    if request.method == "POST":
        nom = request.POST["txtusu"]
        pas = request.POST["txtpas"]

        comprobarLogin = Usuario.objects.filter(nombre_usuario = nom, password_usuario = pas).values()

        if comprobarLogin:
            request.session["estadoSesion"] = True
            request.session["idUsuario"] = comprobarLogin[0]['id']
            request.session["nomUsuario"] = nom.upper()

            datos = { 'nomUsuario' : nom.upper()}

            # Se registra en la tabla historial
            descripcion = "Inicia Sesion"
            tabla = ""
            fechayhora = datetime.now()
            usuario = request.session["idUsuario"]
            his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla,	fecha_hora_historial=fechayhora, usuario_id=usuario )
            his.save()

            if nom.upper() == "ADMIN":
                return render(request, 'menuadmin.html', datos)
            else:
                return render(request, 'menudocente.html', datos)
            
            
        else:
            datos = {'r2' : 'Error De Usuario y/o Contraseña!!'}
            return render(request, 'index.html', datos)

    else:
        datos = { 'r2' : 'No Se Puede Procesar La Solicitud!!'}
        return render(request, 'index.html', datos)
    
#------------------------------------------------------------------------------------------------------------------------------------

def cerrarSesion(request):
    try:
        del request.session["estadoSesion"]
        del request.session["nomUsuario"]

        # Se registra en la tabla historial
        descripcion = "Cierra Sesion"
        tabla = ""
        fechayhora = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla,	fecha_hora_historial=fechayhora, usuario_id=usuario )
        his.save()

        del request.session["idUsuario"]
        return render(request, 'index.html')
    
    except:
        return render(request, 'index.html')
    
#------------------------------------------------------------------------------------------------------------------------------------

def mostrarMenuAdmin(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            datos = {'nomUsuario': nomUsuario} 
            return render(request, 'menuadmin.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}  
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)
    
#------------------------------------------------------------------------------------------------------------------------------------

def mostrarMenuDocente(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() != "ADMIN":
            datos = {'nomUsuario': nomUsuario}  
            return render(request, 'menudocente.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}  
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'} 
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def mostrarCargos(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            cargos = Cargo.objects.all().values()
            datos = {'nomUsuario': nomUsuario, 'cargos' : cargos} 
            return render(request, 'cargos.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}  
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)
    
#------------------------------------------------------------------------------------------------------------------------------------

def registrarCargo(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True and nomUsuario.upper() == "ADMIN":
        # Obtener la lista de cargos
        cargos = Cargo.objects.all()

        if request.method == "POST":
            
            nombre_cargo = request.POST["nombre_cargo"]

            
            if Cargo.objects.filter(nombre_cargo=nombre_cargo).exists():
                datos = {'nomUsuario': nomUsuario, 'cargos': cargos, 'r2': 'El cargo ya existe.'}
                return render(request, 'cargos.html', datos)

            # Crear el cargo y guardarlo en la base de datos
            cargo = Cargo(nombre_cargo=nombre_cargo)
            cargo.save()

            #historial
            descripcion = f"Registro de cargo: {nombre_cargo}"
            tabla = "Cargo"
            fechayhora = datetime.now()
            usuario = request.session["idUsuario"]
            his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
            his.save()

            
            datos = {'nomUsuario': nomUsuario, 'cargos': cargos, 'r': f'Cargo "{nombre_cargo}" registrado correctamente.'}
            return render(request, 'cargos.html', datos)

        else:
            # Renderizar la página de registro de cargos
            datos = {'nomUsuario': nomUsuario, 'cargos': cargos}
            return render(request, 'registrar_cargo.html', datos)

    else:
        datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------    

def actualizarCargo(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            nomUsuario = request.session.get("nomUsuario")
            if nomUsuario == "ADMIN":
                # Obtener el cargo a actualizar
                cargo = Cargo.objects.get(id=id)

                if request.method == "POST":                    
                    nuevo_nombre = request.POST["nuevo_nombre"]
                    cargo.nombre_cargo = nuevo_nombre
                    cargo.save()
                    #historial 
                    descripcion = f"Actualización realizada ({nuevo_nombre.lower()})"
                    tabla = "Cargo"
                    fecha_hora = datetime.now()
                    usuario = request.session["idUsuario"]
                    historial = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fecha_hora, usuario_id=usuario)
                    historial.save()
                    
                    cargos = Cargo.objects.all()
                   
                    datos = {
                        'nomUsuario': request.session["nomUsuario"],
                        'cargos': cargos,
                        'r': 'Cargo Modificado Correctamente!!'
                    }

                    # Redirigir a la página que muestre el listado actualizado
                    return render(request, 'cargos.html', datos)

                else:
                    # Mostrar el formulario de actualización
                    cargos = Cargo.objects.all()

                    datos = {
                        'nomUsuario': request.session["nomUsuario"],
                        'cargos': cargos,
                    }
                    return render(request, 'cargos.html', datos)
                    
            else:
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'r2': 'No Tiene Los Permisos Para Realizar La Accion'
                }
                return render(request, 'index.html', datos)
        else:
            datos = {
                'nomUsuario': request.session["nomUsuario"],
                'r2': 'Debe Iniciar Sesion Para Acceder!!'
            }
            return render(request, 'index.html', datos)
    except Cargo.DoesNotExist:
        cargos = Cargo.objects.all()

        datos = {
            'cargos' :cargos,
            'nomUsuario': request.session["nomUsuario"],
            'r2': f'El ID ({id}) No Existe. Imposible Actualizar!!'
        }
        return render(request, 'cargos.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def mostrarFormActualizarCargo(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            nomUsuario = request.session.get("nomUsuario")
            if nomUsuario == "ADMIN":
                cargo = Cargo.objects.get(id=id)
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'cargo': cargo,
                }
                return render(request, 'form_actualizar_cargo.html', datos)
            else:
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'r2': 'No Tiene Los Permisos Para Realizar La Accion'
                }
                return render(request, 'form_actualizar_cargo.html', datos)
        else:
            datos = {
                'nomUsuario': request.session["nomUsuario"],
                'r2': 'Debe Iniciar Sesion Para Acceder!!'
            }
            return render(request, 'index.html', datos)
    except Cargo.DoesNotExist:
        datos = {
            'nomUsuario': request.session["nomUsuario"],
            'r2': f'El ID ({id}) No Existe. Imposible Actualizar!!'
        }
        return render(request, 'cargos.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def eliminarCargo(request, id):

    estado_sesion = request.session.get("estadoSesion")
    nom_usuario = request.session.get("nomUsuario")

    if estado_sesion is True:
        if nom_usuario.upper() == "ADMIN":
            try:
                cargo = Cargo.objects.get(id=id)
                nombre_cargo = cargo.nombre_cargo
                cargo.delete()

                #tabla historial
                descripcion = f"Eliminación realizada ({nombre_cargo.lower()})"
                tabla = "Cargo"
                fecha_hora = datetime.now()
                usuario = request.session["idUsuario"]
                historial = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fecha_hora, usuario_id=usuario)
                historial.save()

                cargos = Cargo.objects.all()
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'cargos': cargos,
                    'r': f'Cargo ({nombre_cargo}) eliminado correctamente!!'
                }
                return render(request, 'cargos.html', datos)
            except Cargo.DoesNotExist:
                cargos = Cargo.objects.all()
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'cargos': cargos,
                    'r2': f'El ID ({id}) no existe. Imposible eliminar!!'
                }
                return render(request, 'cargos.html', datos)
        else:
            datos = {'r2': 'No tiene permisos suficientes para acceder!!'}
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe iniciar sesión para acceder!!'}
        return render(request, 'index.html', datos)
    
#------------------------------------------------------------------------------------------------------------------------------------

def mostrarCursos(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            cursos = Curso.objects.all()
            datos = {'nomUsuario': nomUsuario, 'cursos' : cursos} 
            return render(request, 'cursos.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}  
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)
    
#------------------------------------------------------------------------------------------------------------------------------------

def registrarCursos(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True and nomUsuario.upper() == "ADMIN":
        # Obtener la lista de cursos
        cursos = Curso.objects.all()

        if request.method == "POST":
            nombre_curso = request.POST["nombre_curso"]

            if Curso.objects.filter(nombre_curso=nombre_curso).exists():
                datos = {'nomUsuario': nomUsuario, 'cursos': cursos, 'r2': 'El curso ya existe.'}
                return render(request, 'cursos.html', datos)
            
            curso = Curso(nombre_curso=nombre_curso)
            curso.save()

            # Historial
            descripcion = f"Registro de curso: {nombre_curso}"
            tabla = "Curso"
            fechayhora = datetime.now()
            usuario = request.session["idUsuario"]
            his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
            his.save()

            datos = {'nomUsuario': nomUsuario, 'cursos': cursos, 'r': f'Curso "{nombre_curso}" registrado correctamente.'}
            return render(request, 'cursos.html', datos)

        else:
            # Renderizar la página de registro de cursos
            datos = {'nomUsuario': nomUsuario, 'cursos': cursos}
            return render(request, 'cursos.html', datos)

    else:
        datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}
        return render(request, 'index.html', datos)
    
#------------------------------------------------------------------------------------------------------------------------------------

def actualizarCurso(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            nomUsuario = request.session.get("nomUsuario")
            if nomUsuario == "ADMIN":
                # Obtener el curso a actualizar
                curso = Curso.objects.get(id=id)

                if request.method == "POST":                    
                    nuevo_nombre = request.POST["nuevo_nombre"]
                    
                    curso.nombre_curso = nuevo_nombre
                    curso.save()

                    # historial 
                    descripcion = f"Actualización realizada ({nuevo_nombre.lower()})"
                    tabla = "Curso"
                    fecha_hora = datetime.now()
                    usuario = request.session["idUsuario"]
                    historial = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fecha_hora, usuario_id=usuario)
                    historial.save()
                    
                    cursos = Curso.objects.all()
                    
                    datos = {
                        'nomUsuario': request.session["nomUsuario"],
                        'cursos': cursos,
                        'r': 'Datos Modificados Correctamente!!'
                    }

                    # Redirigir a la página que muestre el listado actualizado
                    return render(request, 'cursos.html', datos)

                else:
                    # Mostrar el formulario de actualización
                    datos = {
                        'nomUsuario': request.session["nomUsuario"],
                        'curso': curso,
                    }
                    return render(request, 'form_actualizar_curso.html', datos)
                    
            else:
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'r2': 'No Tiene Los Permisos Para Realizar La Accion'
                }
                return render(request, 'index.html', datos)
        else:
            datos = {
                'nomUsuario': request.session["nomUsuario"],
                'r2': 'Debe Iniciar Sesion Para Acceder!!'
            }
            return render(request, 'index.html', datos)
    except Curso.DoesNotExist:
        cursos = Curso.objects.all()
        datos = {
            'nomUsuario': request.session["nomUsuario"],
            'r2': f'El ID ({id}) No Existe. Imposible Actualizar!!',
            'cursos': cursos

        }
        return render(request, 'cursos.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def mostrarFormActualizarCurso(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            nomUsuario = request.session.get("nomUsuario")
            if nomUsuario == "ADMIN":
                curso = Curso.objects.get(id=id)
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'curso': curso,
                }
                return render(request, 'form_actualizar_curso.html', datos)
            else:
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'r2': 'No Tiene Los Permisos Para Realizar La Accion'
                }
                return render(request, 'index.html', datos)
        else:
            datos = {
                'nomUsuario': request.session["nomUsuario"],
                'r2': 'Debe Iniciar Sesion Para Acceder!!'
            }
            return render(request, 'index.html', datos)
    except Curso.DoesNotExist:
        datos = {
            'nomUsuario': request.session["nomUsuario"],
            'r2': f'El ID ({id}) No Existe. Imposible Actualizar!!'
        }
        return render(request, 'cursos.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def eliminarCurso(request, id):
    estado_sesion = request.session.get("estadoSesion")
    nom_usuario = request.session.get("nomUsuario")

    if estado_sesion is True:
        if nom_usuario.upper() == "ADMIN":
            try:
                curso = Curso.objects.get(id=id)
                nombre_curso = curso.nombre_curso
                curso.delete()

                # Tabla historial
                descripcion = f"Eliminación realizada ({nombre_curso.lower()})"
                tabla = "Curso"
                fecha_hora = datetime.now()
                usuario = request.session["idUsuario"]
                historial = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fecha_hora, usuario_id=usuario)
                historial.save()

                cursos = Curso.objects.all()
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'cursos': cursos,
                    'r': f'Registro ({nombre_curso}) eliminado correctamente!!'
                }
                return render(request, 'cursos.html', datos)
            except Curso.DoesNotExist:
                cursos = Curso.objects.all()
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'cursos': cursos,
                    'r2': f'El ID ({id}) no existe. Imposible eliminar!!'
                }
                return render(request, 'cursos.html', datos)
        else:
            datos = {'r2': 'No tiene permisos suficientes para acceder!!'}
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe iniciar sesión para acceder!!'}
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def mostrarAsignaturas(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            asignaturas = Asignatura.objects.all()
            datos = {'nomUsuario': nomUsuario, 'asignaturas' : asignaturas} 
            return render(request, 'asignaturas.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}  
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def crearAsignatura(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True and nomUsuario.upper() == "ADMIN":
        # Obtener la lista de asignaturas
        asignaturas = Asignatura.objects.all()

        if request.method == "POST":
            # Obtener datos del formulario
            nombre_asignatura = request.POST["nombre_asignatura"]
            
            if Asignatura.objects.filter(nombre_asignatura=nombre_asignatura).exists():
                datos = {'nomUsuario': nomUsuario, 'asignaturas': asignaturas, 'r2': 'La asignatura ya existe.'}
                return render(request, 'asignaturas.html', datos)
            
            asignatura = Asignatura(nombre_asignatura=nombre_asignatura)
            asignatura.save()

            #historial
            descripcion = f"Creación de asignatura: {nombre_asignatura}"
            tabla = "Asignatura"
            fechayhora = datetime.now()
            usuario = request.session["idUsuario"]
            his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
            his.save()
            
            datos = {'nomUsuario': nomUsuario, 'asignaturas': asignaturas, 'r': f'Asignatura "{nombre_asignatura}" creada correctamente.'}
            return render(request, 'asignaturas.html', datos)

        else:
            # Renderizar la página 
            datos = {'nomUsuario': nomUsuario, 'asignaturas': asignaturas}
            return render(request, 'crear_asignatura.html', datos)

    else:
        datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def mostrarFormActualizarAsignatura(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            nomUsuario = request.session.get("nomUsuario")
            if nomUsuario == "ADMIN":
                asig = Asignatura.objects.get(id=id)
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'asignatura': asig
                }
                return render(request, 'form_actualizar_asignatura.html', datos)
            else:
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'r2': 'No Tiene Los Permisos Para Realizar La Accion'
                }
                return render(request, 'index.html', datos)
        else:
            datos = {
                'nomUsuario': request.session["nomUsuario"],
                'r2': 'Debe Iniciar Sesion Para Acceder!!'
            }
            return render(request, 'index.html', datos)
    except Curso.DoesNotExist:
        datos = {
            'nomUsuario': request.session["nomUsuario"],
            'r2': f'El ID ({id}) No Existe. Imposible Actualizar!!'
        }
        return render(request, 'asignatura.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def actualizarAsignatura(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            nomUsuario = request.session.get("nomUsuario")
            if nomUsuario == "ADMIN":
                asig = Asignatura.objects.get(id=id)

                if request.method == "POST":                    
                    nuevo_nombre = request.POST["nombre_asignatura"]
                    
                    asig.nombre_asignatura = nuevo_nombre
                    asig.save()

                    # historial 
                    descripcion = f"Actualización realizada ({nuevo_nombre.lower()})"
                    tabla = "Asignatura"
                    fecha_hora = datetime.now()
                    usuario = request.session["idUsuario"]
                    historial = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fecha_hora, usuario_id=usuario)
                    historial.save()
                    
                    asigna = Asignatura.objects.all()
                    
                    datos = {
                        'nomUsuario': request.session["nomUsuario"],
                        'asignaturas': asigna,
                        'r': 'Datos Modificados Correctamente!!'
                    }

                    # Redirigir a la página que muestre el listado actualizado
                    return render(request, 'asignaturas.html', datos)

                else:
                    # Mostrar el formulario de actualización
                    datos = {
                        'nomUsuario': request.session["nomUsuario"],
                        'asignaturas': asigna,
                    }
                    return render(request, 'form_actualizar_asignatura.html', datos)
                    
            else:
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'r2': 'No Tiene Los Permisos Para Realizar La Accion'
                }
                return render(request, 'index.html', datos)
        else:
            datos = {
                'nomUsuario': request.session["nomUsuario"],
                'r2': 'Debe Iniciar Sesion Para Acceder!!'
            }
            return render(request, 'index.html', datos)
    except :
        asigna = Asignatura.objects.all()

        datos = {
            'nomUsuario': request.session["nomUsuario"],
            'r2': f'El ID ({id}) No Existe. Imposible Actualizar!!',
            'asignaturas': asigna

        }
        return render(request, 'asignaturas.html', datos)
    
#------------------------------------------------------------------------------------------------------------------------------------

def eliminarAsignatura(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        nomUsuario = request.session.get("nomUsuario")

        if estadoSesion is True:
            if nomUsuario.upper() == "ADMIN":
                try:
                    asi = Asignatura.objects.get(id=id)
                    nom = asi.nombre_asignatura
                    asi.delete()

                    descripcion = "Eliminacion realizada ("+str(nom.lower())+")"
                    tabla = "Asignatura"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla,	fecha_hora_historial=fechayhora, usuario_id=usuario )
                    his.save()
                    #----------------------

                    asig = Asignatura.objects.all().prefetch_related('funcionarios')
                    asignaturas = Asignatura.objects.all()

                    datos = { 
                        'nomUsuario' : request.session["nomUsuario"],
                        'asig' : asig,
                        'r' : 'Asignatura ('+str(nom)+') Eliminado Correctamente!! ', 'asignaturas' : asignaturas
                        }
                    return render(request, 'asignaturas.html', datos)
                except:
                    asig = Asignatura.objects.all().prefetch_related('funcionarios')
                    datos = { 
                        'nomUsuario' : request.session["nomUsuario"],
                        'asig' : asig,
                        'r2' : 'El ID ('+str(nom)+') No Existe. Imposible Eliminar!! '
                        }
                    return render(request, 'asignaturas.html', datos)
            else:
                datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}  
                return render(request, 'index.html', datos)
        else:
            datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
            return render(request, 'index.html', datos)
    except:
        asigna = Asignatura.objects.all()

        datos = {
            'nomUsuario': request.session["nomUsuario"],
            'r2': f'El ID ({id}) No Existe. Imposible Eliminar!!',
            'asignaturas': asigna

        }
        return render(request, 'asignaturas.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def mostrarFuncionarios(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            opcarg = Cargo.objects.all().values().order_by("nombre_cargo")
            opasig = Asignatura.objects.all().values().order_by("nombre_asignatura")
            opcurs = Curso.objects.all().values().order_by("nombre_curso")
            funcionarios = Funcionario.objects.select_related("cargo", "asignatura", "curso").all().order_by("nombres")

            datos = {'nomUsuario': nomUsuario, 'est': funcionarios, 'opcarg': opcarg, 'opasig': opasig, 'opcurs': opcurs }
            return render(request, 'funcionarios.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def registrarFuncionarios(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":

            if request.method == "POST":
                rut = request.POST["rut"]
                nom = request.POST["nombre"]
                apeP = request.POST["paterno"]
                apeM = request.POST["materno"]
                ema = request.POST["correo"]
                car = request.POST["cargo"]
                cursos_input = request.POST["cursos"]
                jefatura_input = request.POST["jefatura"]
                asignaturas_input = request.POST["asignaturas"]           
                

                comprobarFuncionario = Funcionario.objects.filter(rut = rut)
                if comprobarFuncionario:
                    est = Funcionario.objects.select_related("cargo", "asignatura", "curso").all().order_by("nombres")
                    opcarg = Cargo.objects.all().values().order_by("nombre_cargo")
                    opasig = Asignatura.objects.all().values().order_by("nombre_asignatura")
                    opcurs = Curso.objects.all().values().order_by("nombre_curso")

                    datos = {
                        'nomUsuario' : nomUsuario,
                        'est' : est,
                        'opcarg': opcarg, 'opasig': opasig, 'opcurs': opcurs,
                        'r2' : 'El Funcionario con el RUT ('+str(rut.upper())+') Ya Existe!! '
                        }
                    return render(request, 'funcionarios.html', datos)
                
                else:
                    fun = Funcionario(rut=rut,nombres=nom,paterno=apeP,materno=apeM,correo=ema,cargo_id=car, curso_id=cursos_input, jefatura_id=jefatura_input, asignatura_id=asignaturas_input)
                    fun.save()
 
                    opcarg = Cargo.objects.all().values().order_by("nombre_cargo")
                    opasig = Asignatura.objects.all().values().order_by("nombre_asignatura")
                    opcurs = Curso.objects.all().values().order_by("nombre_curso")

                    descripcion = "Insert realizado ("+str(nom.lower())+")"
                    tabla = "Funcionario"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla,	fecha_hora_historial=fechayhora, usuario_id=usuario )
                    his.save()

                    est = Funcionario.objects.select_related("cargo", "asignatura", "curso").all().order_by("nombres")

                    datos = { 
                        'nomUsuario' : nomUsuario,
                        'est' : est,
                        'r' : 'Funcionario '+str(nom)+ ' Registrado Correctamente!!', 'opcarg': opcarg, 'opasig': opasig, 'opcurs': opcurs
                        }
                    return render(request, 'funcionarios.html', datos)
            else:
                est = Funcionario.objects.select_related("cargo", "asignatura", "curso").all().order_by("nombres")
                opcarg = Cargo.objects.all().values().order_by("nombre_cargo")
                opasig = Asignatura.objects.all().values().order_by("nombre_asignatura")
                opcurs = Curso.objects.all().values().order_by("nombre_curso")
                datos = { 
                    'nomUsuario' : nomUsuario,
                    'est' : est,
                    'r2' : 'Debe Presionar El Boton Para Registrar Un Funcionario!! ',
                    'opcarg': opcarg, 'opasig': opasig, 'opcurs': opcurs
                    }
                return render(request, 'funcionarios.html', datos)
        else:
            
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}  
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'} 
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def mostrarFormActualizarFuncionario(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            nomUsuario = request.session.get("nomUsuario")
            if nomUsuario == "ADMIN":
                encontrado = Funcionario.objects.get(id=id)
                opcarg = Cargo.objects.all().values().order_by("nombre_cargo")
                opasig = Asignatura.objects.all().values().order_by("nombre_asignatura")
                opcurs = Curso.objects.all().values().order_by("nombre_curso")

                est = Funcionario.objects.all().select_related("cargo", "asignatura", "curso").all().order_by("nombres")

                datos = {
                    'nomUsuario' : request.session["nomUsuario"],
                    'encontrado' : encontrado,
                    'est' : est,
                    'opcarg': opcarg, 'opasig': opasig, 'opcurs': opcurs
                }

                return render(request, 'form_actualizar_funcionario.html', datos)

            else:
                est = Funcionario.objects.all().values()

                datos = {
                    'nomUsuario' : request.session["nomUsuario"],
                    'est' : est,
                    'r2' : 'No Tiene Los Permisos Para Realizar La Accion'
                }

                return render(request, 'index.html', datos)
        else:
            est = Funcionario.objects.all().values()

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'est' : est,
                'r2' : 'Debe Iniciar Sesion Para Acceder!!'
            }

            return render(request, 'index.html', datos)
    
    except:
        est = Funcionario.objects.all().select_related("cargo", "asignatura", "curso").all().order_by("nombres")
        opcarg = Cargo.objects.all().values().order_by("nombre_cargo")
        opasig = Asignatura.objects.all().values().order_by("nombre_asignatura")
        opcurs = Curso.objects.all().values().order_by("nombre_curso")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'est' : est,
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar!!',
            'opcarg': opcarg, 'opasig': opasig, 'opcurs': opcurs

        }

        return render(request, 'funcionarios.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def actualizarFuncionario(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            nomUsuario = request.session.get("nomUsuario")
            if nomUsuario == "ADMIN":
                if request.method == "POST":
                    # Recuperar los datos del formulario
                    rut = request.POST["rut"]
                    nom = request.POST["nombre"]
                    pat = request.POST["paterno"]
                    mat = request.POST["materno"]
                    correo = request.POST["correo"]
                    cargo = request.POST["cargo"]

                    # Recuperar las listas de cursos, jefaturas y asignaturas
                    cursos_input = request.POST["curso"]
                    jefatura_input = request.POST["jefatura"]
                    asignaturas_input = request.POST["asignatura"]



                    # Obtener el objeto Funcionario a actualizar
                    est = Funcionario.objects.get(id=id)


                    # Actualizar los campos del objeto
                    est.rut = rut
                    est.nombres = nom
                    est.paterno = pat
                    est.materno = mat
                    est.correo = correo
                    est.cargo_id = cargo
                    est.asignatura_id = asignaturas_input
                    est.curso_id = cursos_input
                    est.jefatura_id = jefatura_input


                    est.save()

                    nombre_completo = f"{est.nombres} {est.paterno} {est.materno}"

                    descripcion = f"Actualización realizada ({nom.lower()} {pat.lower()} {mat.lower()})"
                    tabla = "Funcionario"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
                    his.save()

                    funcionarios = Funcionario.objects.select_related("cargo", "asignatura", "curso").all().order_by("nombres")
                    opcarg = Cargo.objects.all().values().order_by("nombre_cargo")
                    opasig = Asignatura.objects.all().values().order_by("nombre_asignatura")
                    opcurs = Curso.objects.all().values().order_by("nombre_curso")
                    datos = {
                        'nomUsuario': request.session["nomUsuario"],
                        'est': funcionarios,
                        'opcarg': opcarg, 'opasig': opasig, 'opcurs': opcurs,
                        'r': f'Datos de Funcionario {nombre_completo} Modificados Correctamente!!'
                    }

                    return render(request, 'funcionarios.html', datos)
                else:
                    est = Funcionario.objects.select_related("cargo", "asignatura", "curso").all().order_by("nombres")
                    opcarg = Cargo.objects.all().values().order_by("nombre_cargo")
                    opasig = Asignatura.objects.all().values().order_by("nombre_asignatura")
                    opcurs = Curso.objects.all().values().order_by("nombre_curso")
                
                    datos = {
                        'nomUsuario' : request.session["nomUsuario"],
                        'opcarg': opcarg, 'opasig': opasig, 'opcurs': opcurs,

                        'est' : est,
                        'r2' : 'El ID('+str(id)+') No Existe. Imposible Mostrar Datos'
                    }

                    return render(request, 'funcionarios.html', datos)
            else:
                est = Funcionario.objects.select_related("cargo", "asignatura", "curso").all().order_by("nombres")

                datos = {
                    'nomUsuario' : request.session["nomUsuario"],

                    'est' : est,
                    'r2' : 'No Tiene Los Permisos Para Realizar La Accion'
                }

                return render(request, 'index.html', datos)
        else:
            est = Funcionario.objects.select_related("cargo", "asignatura", "curso").all().order_by("nombres")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'est' : est,
                'r2' : 'Debe Iniciar Sesion Para Acceder!!'
            }
            return render(request, 'index.html', datos)
        
    except:
        est = Funcionario.objects.select_related("cargo", "asignatura", "curso").all().order_by("nombres")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'est' : est,
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar!!'
        }

        return render(request, 'funcionarios.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def eliminarFuncionario(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            try:
                fun = Funcionario.objects.get(id=id)
                nom = fun.nombres
                fun.delete()

                #Se registra en la tabla historial 

                descripcion = "Eliminacion realizada ("+str(nom.lower())+")"
                tabla = "Funcionario"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla,	fecha_hora_historial=fechayhora, usuario_id=usuario )
                his.save()

                est = Funcionario.objects.select_related("cargo", "asignatura", "curso").all().order_by("nombres")

                opcarg = Cargo.objects.all().values().order_by("nombre_cargo")
                opasig = Asignatura.objects.all().values().order_by("nombre_asignatura")
                opcurs = Curso.objects.all().values().order_by("nombre_curso")

                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'est' : est,
                    'r' : 'Registro ('+str(nom)+') Eliminado Correctamente!! ',
                    'opcarg': opcarg, 'opasig': opasig, 'opcurs': opcurs
                    }
                return render(request, 'funcionarios.html', datos)
            except:
                est = Funcionario.objects.select_related("cargo", "asignatura", "curso").all().order_by("nombres")

                opcarg = Cargo.objects.all().values().order_by("nombre_cargo")
                opasig = Asignatura.objects.all().values().order_by("nombre_asignatura")
                opcurs = Curso.objects.all().values().order_by("nombre_curso")

                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'est' : est,
                    'opcarg': opcarg, 'opasig': opasig, 'opcurs': opcurs,
                    'r2' : 'El ID('+str(id)+') No Existe. Imposible Eliminar!! '
                    }
                return render(request, 'funcionarios.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}  
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------
#FiltrosFuncionarios

def filtroEmpieza(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            filtro = request.POST['txtfil']
            est = Funcionario.objects.filter(nombres__startswith=filtro).select_related("cargo", "asignatura", "curso").all()
            opcarg = Cargo.objects.all().values().order_by("nombre_cargo")
            opasig = Asignatura.objects.all().values().order_by("nombre_asignatura")
            opcurs = Curso.objects.all().values().order_by("nombre_curso")
            datos = {'est': est, 'nomUsuario': nomUsuario,'opcarg': opcarg, 'opasig': opasig, 'opcurs': opcurs}
            return render(request, 'funcionarios.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'
                    } 
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def filtroContenga(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            filtro = request.POST['txtfil']
            opcarg = Cargo.objects.all().values().order_by("nombre_cargo")
            opasig = Asignatura.objects.all().values().order_by("nombre_asignatura")
            opcurs = Curso.objects.all().values().order_by("nombre_curso")            
            est = Funcionario.objects.filter(nombres__contains=filtro).select_related("cargo", "asignatura", "curso").all()
            datos = {'est': est, 'nomUsuario': nomUsuario,'opcarg': opcarg, 'opasig': opasig, 'opcurs': opcurs}
            return render(request, 'funcionarios.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'} 
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def filtroTermina(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            filtro = request.POST['txtfil']
            opcarg = Cargo.objects.all().values().order_by("nombre_cargo")
            opasig = Asignatura.objects.all().values().order_by("nombre_asignatura")
            opcurs = Curso.objects.all().values().order_by("nombre_curso")            
            est = Funcionario.objects.filter(nombres__endswith=filtro).select_related("cargo", "asignatura", "curso").all()
            datos = {'est': est, 'nomUsuario': nomUsuario,'opcarg': opcarg, 'opasig': opasig, 'opcurs': opcurs}
            return render(request, 'funcionarios.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'} 
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def filtroOrden(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    opcion = request.POST['cboopt']
    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            opcarg = Cargo.objects.all().values().order_by("nombre_cargo")
            opasig = Asignatura.objects.all().values().order_by("nombre_asignatura")
            opcurs = Curso.objects.all().values().order_by("nombre_curso")
            if opcion == 'ascendente':
                est = Funcionario.objects.all().order_by('id').select_related("cargo", "asignatura", "curso").all()
            elif opcion == 'descendente':
                est = Funcionario.objects.all().order_by('-id').select_related("cargo", "asignatura", "curso").all()
            datos = {'est': est, 'nomUsuario': nomUsuario,'opcarg': opcarg, 'opasig': opasig, 'opcurs': opcurs}
            return render(request, 'funcionarios.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'} 
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def mostrarNacionalidades(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            nacionalidades = Nacionalidad.objects.all()
            datos = {'nomUsuario': nomUsuario, 'nacionalidades' : nacionalidades} 
            return render(request, 'nacionalidades.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}  
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def registrarNacionalidades(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True and nomUsuario.upper() == "ADMIN":
        nacionalidades = Nacionalidad.objects.all()

        if request.method == "POST":
            nombre_nacionalidad = request.POST["nombre_nacionalidad"]

            nacionalidad = Nacionalidad(nombre_nacionalidad=nombre_nacionalidad)
            nacionalidad.save()

            descripcion = f"Registro de nacionalidad: {nombre_nacionalidad}"
            tabla = "Nacionalidad"
            fechayhora = datetime.now()
            usuario = request.session["idUsuario"]
            his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
            his.save()

            datos = {'nomUsuario': nomUsuario, 'nacionalidades': nacionalidades, 'r': f'Nacionalidad "{nombre_nacionalidad}" registrada correctamente.'}
            return render(request, 'nacionalidades.html', datos)

        else:
            datos = {'nomUsuario': nomUsuario, 'nacionalidades': nacionalidades}
            return render(request, 'nacionalidades.html', datos)

    else:
        datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def mostrarFormActualizarNacionalidad(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            nomUsuario = request.session.get("nomUsuario")
            if nomUsuario == "ADMIN":
                nacionalidad = Nacionalidad.objects.get(id=id)
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'nacionalidad': nacionalidad,
                }
                return render(request, 'form_actualizar_nacionalidad.html', datos)
            else:
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'r2': 'No Tiene Los Permisos Para Realizar La Accion'
                }
                return render(request, 'index.html', datos)
        else:
            datos = {
                'nomUsuario': request.session["nomUsuario"],
                'r2': 'Debe Iniciar Sesion Para Acceder!!'
            }
            return render(request, 'index.html', datos)
    except Nacionalidad.DoesNotExist:
        datos = {
            'nomUsuario': request.session["nomUsuario"],
            'r2': f'El ID ({id}) No Existe. Imposible Actualizar!!'
        }
        return render(request, 'nacionalidades.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def actualizarNacionalidad(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            nomUsuario = request.session.get("nomUsuario")
            if nomUsuario == "ADMIN":
                nacionalidad = Nacionalidad.objects.get(id=id)

                nuevo_nombre = request.POST["nuevo_nombre"]
                nacionalidad.nombre_nacionalidad = nuevo_nombre
                nacionalidad.save()

                #historial
                descripcion = f"Actualización realizada ({nuevo_nombre.lower()})"
                tabla = "Nacionalidad"
                fecha_hora = datetime.now()
                usuario = request.session["idUsuario"]
                historial = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fecha_hora, usuario_id=usuario)
                historial.save()

                nacionalidades = Nacionalidad.objects.all()

                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'nacionalidades': nacionalidades,
                    'r': 'Datos Modificados Correctamente!!'
                }

                # Redirigir a la página que muestre el listado actualizado
                return render(request, 'nacionalidades.html', datos)
            else:
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'r2': 'No Tiene Los Permisos Para Realizar La Accion'
                }
                return render(request, 'index.html', datos)
        else:
            datos = {
                'nomUsuario': request.session["nomUsuario"],
                'r2': 'Debe Iniciar Sesion Para Acceder!!'
            }
            return render(request, 'index.html', datos)
    except Nacionalidad.DoesNotExist:
        nacionalidades = Nacionalidad.objects.all()

        datos = {
            'nomUsuario': request.session["nomUsuario"],
            'r2': f'El ID ({id}) No Existe. Imposible Actualizar!!',
            'nacionalidades': nacionalidades

        }
        return render(request, 'nacionalidades.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def eliminarNacionalidad(request, id):
    estado_sesion = request.session.get("estadoSesion")
    nom_usuario = request.session.get("nomUsuario")

    if estado_sesion is True:
        if nom_usuario.upper() == "ADMIN":
            try:
                nacionalidad = Nacionalidad.objects.get(id=id)
                nombre_nacionalidad = nacionalidad.nombre_nacionalidad
                nacionalidad.delete()

                descripcion = f"Eliminación realizada ({nombre_nacionalidad.lower()})"
                tabla = "Nacionalidad"
                fecha_hora = datetime.now()
                usuario = request.session["idUsuario"]
                historial = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fecha_hora, usuario_id=usuario)
                historial.save()

                nacionalidades = Nacionalidad.objects.all()
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'nacionalidades': nacionalidades,
                    'r': f'Registro ({nombre_nacionalidad}) eliminado correctamente!!'
                }
                return render(request, 'nacionalidades.html', datos)
            except Nacionalidad.DoesNotExist:
                nacionalidades = Nacionalidad.objects.all()
                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'nacionalidades': nacionalidades,
                    'r2': f'El ID ({id}) no existe. Imposible eliminar!!'
                }
                return render(request, 'nacionalidades.html', datos)
        else:
            datos = {'r2': 'No tiene permisos suficientes para acceder!!'}
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe iniciar sesión para acceder!!'}
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def mostrarMatricula(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            opnacinalidades = Nacionalidad.objects.all().values().order_by("nombre_nacionalidad")
            opcionescursos = Curso.objects.all().values().order_by("nombre_curso")
            matriculas = Matricula.objects.all().select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all().order_by("estudiante_nombres")
            datos = {'nomUsuario': nomUsuario, 'est': matriculas, 'opnac': opnacinalidades, 'opcur' : opcionescursos} 
            return render(request, 'matricula.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}  
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)
    
#------------------------------------------------------------------------------------------------------------------------------------

def registrarMatricula(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":

            if request.method == "POST":
                apoderado_rut = request.POST["apoderado_rut"]
                apoderado_nombres = request.POST["apoderado_nombres"]
                apoderado_paterno = request.POST["apoderado_paterno"]
                apoderado_materno = request.POST["apoderado_materno"]
                apoderado_edad = int(request.POST["apoderado_edad"])  # Asegúrate de tener el campo correcto
                apoderado_parentesco = request.POST["apoderado_parentesco"]
                apoderado_nacionalidades_input = request.POST["apoderado_nacionalidades"]
                estudiante_rut = request.POST["estudiante_rut"]
                estudiante_nombres = request.POST["estudiante_nombres"]
                estudiante_paterno = request.POST["estudiante_paterno"]
                estudiante_materno = request.POST["estudiante_materno"]
                estudiante_edad = int(request.POST["estudiante_edad"])  # Asegúrate de tener el campo correcto
                estudiante_nacionalidades_input = request.POST["estudiante_nacionalidades"]
                cursos_input = request.POST["curso"]

                comprobarMatricula = Matricula.objects.filter(estudiante_rut = estudiante_rut)
                if comprobarMatricula:
                    matriculas = Matricula.objects.all().select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all().order_by("estudiante_nombres")
                    opnacinalidades = Nacionalidad.objects.all().values().order_by("nombre_nacionalidad")
                    opcionescursos = Curso.objects.all().values().order_by("nombre_curso")

                    datos = {
                        'nomUsuario' : nomUsuario,
                        'est' : matriculas,
                        'opnac': opnacinalidades, 'opcur' : opcionescursos,

                        'r2' : 'La Matricula con el RUT ('+str(estudiante_rut.upper())+') Ya Existe!! '
                        }
                    return render(request, 'matricula.html', datos)
                
                else:
                    # Crear y guardar la matrícula
                    matricula = Matricula(
                        apoderado_rut=apoderado_rut,
                        apoderado_nombres=apoderado_nombres,
                        apoderado_paterno=apoderado_paterno,
                        apoderado_materno=apoderado_materno,
                        apoderado_edad=apoderado_edad,
                        apoderado_parentesco=apoderado_parentesco,
                        apoderado_nacionalidad_id=apoderado_nacionalidades_input,
                        estudiante_rut=estudiante_rut,
                        estudiante_nombres=estudiante_nombres,
                        estudiante_paterno=estudiante_paterno,
                        estudiante_materno=estudiante_materno,
                        estudiante_edad=estudiante_edad,
                        estudiante_nacionalidad_id = estudiante_nacionalidades_input,
                        curso_id = cursos_input
                    )
                    opnacinalidades = Nacionalidad.objects.all().values().order_by("nombre_nacionalidad")
                    opcionescursos = Curso.objects.all().values().order_by("nombre_curso")

                    # Guardar la matrícula
                    matricula.save()
                    # Registro en la tabla historial
                    descripcion = "Matrícula realizada para " + estudiante_nombres
                    tabla = "Matricula"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla,
                                    fecha_hora_historial=fechayhora, usuario_id=usuario)
                    his.save()

                    matriculas = Matricula.objects.all().select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all().order_by("estudiante_nombres")

                    datos = {
                        'nomUsuario': nomUsuario,
                        'est': matriculas,
                        'r': 'Matrícula realizada para ' + estudiante_nombres + ' correctamente!!',
                        'opnac': opnacinalidades, 'opcur' : opcionescursos
                    }
                    return render(request, 'matricula.html', datos)
            else:
                matriculas = Matricula.objects.all().select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all().order_by("estudiante_nombres")
                opnacinalidades = Nacionalidad.objects.all().values().order_by("nombre_nacionalidad")
                opcionescursos = Curso.objects.all().values().order_by("nombre_curso")

                datos = {
                    'nomUsuario': nomUsuario,
                    'matriculas': matriculas,
                    'opnac': opnacinalidades, 'opcur' : opcionescursos,

                    'r2': 'Debe completar el formulario para realizar una matrícula!! '
                }
                return render(request, 'matricula.html', datos)
        else:
            datos = {'r2': 'No tiene permisos suficientes para acceder!!'}
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe iniciar sesión para acceder!!'}
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def mostrarFormActualizarMatricula(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            nomUsuario = request.session.get("nomUsuario")
            if nomUsuario == "ADMIN":
                encontrado = Matricula.objects.get(id=id)

                opnacinalidades = Nacionalidad.objects.all().values().order_by("nombre_nacionalidad")
                opcionescursos = Curso.objects.all().values().order_by("nombre_curso")
                est = Matricula.objects.all().select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all().order_by("estudiante_nombres")

                datos = {
                    'nomUsuario' : request.session["nomUsuario"],
                    'encontrado' : encontrado,
                    'est' : est,
                    'opnac': opnacinalidades, 'opcur' : opcionescursos
                }

                return render(request, 'form_actualizar_matricula.html', datos)

            else:
                est = Matricula.objects.all().select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all().order_by("estudiante_nombres")

                datos = {
                    'nomUsuario' : request.session["nomUsuario"],
                    'est' : est,
                    'r2' : 'No Tiene Los Permisos Para Realizar La Accion'
                }

                return render(request, 'index.html', datos)
        else:
            est = Matricula.objects.all().select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all().order_by("estudiante_nombres")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'est' : est,
                'r2' : 'Debe Iniciar Sesion Para Acceder!!'
            }

            return render(request, 'index.html', datos)
    
    except:
        est = Matricula.objects.all().select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all().order_by("estudiante_nombres")
        opnacinalidades = Nacionalidad.objects.all().values().order_by("nombre_nacionalidad")
        opcionescursos = Curso.objects.all().values().order_by("nombre_curso")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'est' : est,
            'opnac': opnacinalidades, 'opcur' : opcionescursos,
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar!!'
        }

        return render(request, 'matricula.html', datos)
    
#------------------------------------------------------------------------------------------------------------------------------------

def actualizarMatricula(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":

            if request.method == "POST":
                apoderado_rut = request.POST["apoderado_rut"]
                apoderado_nombres = request.POST["apoderado_nombres"]
                apoderado_paterno = request.POST["apoderado_paterno"]
                apoderado_materno = request.POST["apoderado_materno"]
                apoderado_edad = int(request.POST["apoderado_edad"])  # Asegúrate de tener el campo correcto
                apoderado_parentesco = request.POST["apoderado_parentesco"]
                apoderado_nacionalidades_input = request.POST["apoderado_nacionalidades"]
                estudiante_rut = request.POST["estudiante_rut"]
                estudiante_nombres = request.POST["estudiante_nombres"]
                estudiante_paterno = request.POST["estudiante_paterno"]
                estudiante_materno = request.POST["estudiante_materno"]
                estudiante_edad = int(request.POST["estudiante_edad"])  # Asegúrate de tener el campo correcto
                estudiante_nacionalidades_input = request.POST["estudiante_nacionalidades"]
                cursos_input = request.POST["curso"]
                mat = Matricula.objects.get(id=id)

                mat.apoderado_rut = apoderado_rut
                mat.apoderado_nombres = apoderado_nombres
                mat.apoderado_paterno = apoderado_paterno
                mat.apoderado_materno = apoderado_materno
                mat.apoderado_edad = apoderado_edad
                mat.apoderado_parentesco = apoderado_parentesco
                mat.apoderado_nacionalidad_id = apoderado_nacionalidades_input
                mat.estudiante_rut = estudiante_rut
                mat.estudiante_nombres = estudiante_nombres
                mat.estudiante_rut = estudiante_rut
                mat.estudiante_paterno = estudiante_paterno
                mat.estudiante_materno = estudiante_materno
                mat.estudiante_edad = estudiante_edad
                mat.estuidante_nacionalidad_id = estudiante_nacionalidades_input
                mat.curso_id = cursos_input

                # Asignar el nuevo curso a la matrícula

                mat.save()

                # Registro en la tabla historial
                descripcion = "Matrícula actualizada para " + estudiante_nombres
                tabla = "Matricula"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla,
                                fecha_hora_historial=fechayhora, usuario_id=usuario)
                his.save()

                matriculas = Matricula.objects.all().select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all().order_by("estudiante_nombres")
                opnacinalidades = Nacionalidad.objects.all().values().order_by("nombre_nacionalidad")
                opcionescursos = Curso.objects.all().values().order_by("nombre_curso")

                datos = {
                    'nomUsuario': nomUsuario,
                    'est': matriculas,
                    'opnac': opnacinalidades, 'opcur' : opcionescursos,
                    'r': 'Matrícula actualizada para ' + estudiante_nombres + ' correctamente!!'
                }
                return render(request, 'matricula.html', datos)
            else:
                matriculas = Matricula.objects.all().select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all().order_by("estudiante_nombres")
                opnacinalidades = Nacionalidad.objects.all().values().order_by("nombre_nacionalidad")
                opcionescursos = Curso.objects.all().values().order_by("nombre_curso")

                datos = {
                    'nomUsuario': nomUsuario,
                    'est': matriculas,
                    'opnac': opnacinalidades, 'opcur' : opcionescursos,
                    'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar!!'
                }
                return render(request, 'matricula.html', datos)
        else:
            datos = {'r2': 'No tiene permisos suficientes para acceder!!'}
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe iniciar sesión para acceder!!'}
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def eliminarMatricula(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            try:
                matricula = Matricula.objects.get(id=id)
                nombre_estudiante = matricula.estudiante_nombres

                # Eliminar la matrícula
                matricula.delete()

                # Registro en la tabla historial
                descripcion = "Eliminación realizada para la matrícula de " + nombre_estudiante
                tabla = "Matricula"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla,
                                fecha_hora_historial=fechayhora, usuario_id=usuario)
                his.save()

                matriculas = Matricula.objects.all().select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all().order_by("estudiante_nombres")
                opnacinalidades = Nacionalidad.objects.all().values().order_by("nombre_nacionalidad")
                opcionescursos = Curso.objects.all().values().order_by("nombre_curso")

                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'est': matriculas,
                    'opnac': opnacinalidades, 'opcur' : opcionescursos,
                    'r': 'Matrícula de ' + nombre_estudiante + ' eliminada correctamente!!'
                }
                return render(request, 'matricula.html', datos)
            except Matricula.DoesNotExist:
                matriculas = Matricula.objects.all().select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all().order_by("estudiante_nombres")
                opnacinalidades = Nacionalidad.objects.all().values().order_by("nombre_nacionalidad")
                opcionescursos = Curso.objects.all().values().order_by("nombre_curso")

                datos = {
                    'nomUsuario': request.session["nomUsuario"],
                    'est': matriculas,
                    'opnac': opnacinalidades, 'opcur' : opcionescursos,
                    'r2': 'El ID (' + str(id) + ') no existe. Imposible eliminar!!'
                }
                return render(request, 'matricula.html', datos)
        else:
            datos = {'r2': 'No tiene permisos suficientes para acceder!!'}
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe iniciar sesión para acceder!!'}
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------
#FiltrosMatriculas

def filtroEmpiezaMatricula(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            filtro = request.POST['txtfil']
            opnacinalidades = Nacionalidad.objects.all().values().order_by("nombre_nacionalidad")
            opcionescursos = Curso.objects.all().values().order_by("nombre_curso")

            est = Matricula.objects.filter(estudiante_nombres__startswith=filtro).select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all().order_by("estudiante_nombres")
            datos = {'est': est, 'nomUsuario': nomUsuario, 'opnac': opnacinalidades, 'opcur' : opcionescursos,
}
            return render(request, 'matricula.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'} 
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def filtroContengaMatricula(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            filtro = request.POST['txtfil']
            opnacinalidades = Nacionalidad.objects.all().values().order_by("nombre_nacionalidad")
            opcionescursos = Curso.objects.all().values().order_by("nombre_curso")

            est = Matricula.objects.filter(estudiante_nombres__contains=filtro).select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all()
            datos = {'est': est, 'nomUsuario': nomUsuario,
                    'opnac': opnacinalidades, 'opcur' : opcionescursos,}
            return render(request, 'matricula.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'} 
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def filtroTerminaMatricula(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            filtro = request.POST['txtfil']
            opnacinalidades = Nacionalidad.objects.all().values().order_by("nombre_nacionalidad")
            opcionescursos = Curso.objects.all().values().order_by("nombre_curso")

            est = Matricula.objects.filter(estudiante_nombres__endswith=filtro).select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all()
            datos = {'est': est, 'nomUsuario': nomUsuario,'opnac': opnacinalidades, 'opcur' : opcionescursos,}
            return render(request, 'matricula.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'} 
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def filtroOrdenMatricula(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    opcion = request.POST['cboopt']
    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            opnacinalidades = Nacionalidad.objects.all().values().order_by("nombre_nacionalidad")
            opcionescursos = Curso.objects.all().values().order_by("nombre_curso")

            if opcion == 'ascendente':
                est = Matricula.objects.all().order_by('id').select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all()
            elif opcion == 'descendente':
                est = Matricula.objects.all().order_by('-id').select_related("apoderado_nacionalidad", "estudiante_nacionalidad", "curso").all()
            datos = {'est': est, 'nomUsuario': nomUsuario,'opnac': opnacinalidades, 'opcur' : opcionescursos,}
            return render(request, 'matricula.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'} 
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def mostrarHistorial(request):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["nomUsuario"].upper() == "ADMIN":
                his = Historial.objects.select_related("usuario").all().order_by("-fecha_hora_historial")
                datos = {
                    'nomUsuario' : request.session["nomUsuario"],
                    'his' : his
                }
                return render(request, 'historial.html', datos)


            else:
                datos = { 'r2' : 'No tiene Permisos Suficientes Para Acceder.'}  
                return render(request, 'index.html', datos)

        else:
            datos =  { 'r2' : 'Debe Iniciar Sesión Para Acceder!'}  
            return render(request, 'index.html', datos)

    except:
            datos = { 'r2' : 'Error Al Obtener Historial!'}  
            return render(request, 'index.html', datos)
        
#------------------------------------------------------------------------------------------------------------------------------------

def mostrarPerfil(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            usuario_id = request.session["idUsuario"]  # Obtener el ID del usuario desde la sesión
            usuario = Usuario.objects.get(id=usuario_id)  # Obtener el objeto Usuario usando el ID

            

            descripcion = "Ver Perfil"
            tabla = ""
            fechayhora = datetime.now()
            usuario_id = request.session["idUsuario"]
            his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario_id)
            his.save()

            mostrar_contraseña = request.GET.get('mostrar_contraseña', '')
            if mostrar_contraseña == 'si':
                usuario.password_visible = usuario.password_usuario

            return render(request, "perfil.html", {'usu': usuario, 'rol': nomUsuario.upper(), 'mostrar_contraseña': mostrar_contraseña})

        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------


def mostrarCambiarClave(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        nomUsuario = request.session.get("nomUsuario")
        if estadoSesion is True:
            if nomUsuario.upper() == "ADMIN":
                usu = Usuario.objects.get(id=id)

                datos = {'nomUsuario': nomUsuario, 'usu': usu, 'rol': nomUsuario} 
                return render(request, 'cambiarclave.html', datos)
            else:
                datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}  
                return render(request, 'index.html', datos)
        else:
            datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
            return render(request, 'index.html', datos)
    except:
        mostrar_contraseña = request.GET.get('mostrar_contraseña', '')
        if mostrar_contraseña == 'si':
            usu.password_visible = usu.password_usuario

        datos = {
            'nomUsuario': request.session["nomUsuario"], 'rol': nomUsuario,
            'r2': f'El ID ({id}) No Existe. Imposible Actualizar Clave!!',
            'mostrar_contraseña': mostrar_contraseña
        }
        return render(request, 'perfil.html', datos)
#------------------------------------------------------------------------------------------------------------------------------------

def actualizarClave(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        nomUsuario = request.session.get("nomUsuario")
        if estadoSesion is True:
            if nomUsuario.upper() == "ADMIN":
                usu = Usuario.objects.get(id=id)
                if request.method == "POST" :                    
                    nueva_clave = request.POST["nueva_clave"]
                    confirmar_clave = request.POST["confirmar_clave"]
                    if nueva_clave == confirmar_clave:
                        usu.password_usuario = nueva_clave
                        usu.save()

                        # historial 
                        descripcion = f"Actualización de clave realizada ({usu.nombre_usuario.lower()})"
                        tabla = "Usuario"
                        fecha_hora = datetime.now()
                        usuario = request.session["idUsuario"]
                        historial = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fecha_hora, usuario_id=usuario)
                        historial.save()
                        
                        mostrar_contraseña = request.GET.get('mostrar_contraseña', '')
                        if mostrar_contraseña == 'si':
                            usu.password_visible = usu.password_usuario
                        
                        datos = {
                            'nomUsuario': nomUsuario,
                            'usu' : usu,
                            'rol': nomUsuario,
                            'mostrar_contraseña': mostrar_contraseña,
                            'r': f'Clave de usuario({usu.nombre_usuario}) Actualizada Correctamente!!'
                        }

                        # Redirigir a la página que muestre el listado actualizado
                        return render(request, 'perfil.html', datos)
                    else:
                        mostrar_contraseña = request.GET.get('mostrar_contraseña', '')
                        if mostrar_contraseña == 'si':
                            usu.password_visible = usu.password_usuario
                        datos = {
                            'nomUsuario': nomUsuario,
                            'usu' : usu,
                            'rol': nomUsuario,
                            'mostrar_contraseña': mostrar_contraseña,
                            'r2': f'Clave de usuario({usu.nombre_usuario}) No Coinciden!!'
                        }
                        return render(request, 'perfil.html', datos)
                else:
                    mostrar_contraseña = request.GET.get('mostrar_contraseña', '')
                    if mostrar_contraseña == 'si':
                        usu.password_visible = usu.password_usuario                   
                    datos = {'nomUsuario': nomUsuario,
                        'usu' : usu,
                        'rol': nomUsuario,
                        'mostrar_contraseña': mostrar_contraseña,
                        'r2' : 'El ID('+str(id)+') No Existe. Imposible Mostrar Datos'
                    }
                    return render(request, 'perfil.html', datos)
            else:
                datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}  
                return render(request, 'index.html', datos)
        else:
            datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
            return render(request, 'index.html', datos)
    except:
        if mostrar_contraseña == 'si':
            usu.password_visible = usu.password_usuario     
        datos = {
            'nomUsuario': request.session["nomUsuario"],
            'rol': nomUsuario,
            'mostrar_contraseña': mostrar_contraseña,
            'r2': f'El ID ({id}) No Existe. Imposible Actualizar Clave!!'
        }
        return render(request, 'perfil.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def mostrarPerfilDocente(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "DOCENTE":
            usuario_id = request.session["idUsuario"]  # Obtener el ID del usuario desde la sesión
            usuario = Usuario.objects.get(id=usuario_id)  # Obtener el objeto Usuario usando el ID

            
            descripcion = "Ver Perfil Docente"
            tabla = ""
            fechayhora = datetime.now()
            usuario_id = request.session["idUsuario"]
            his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario_id)
            his.save()

            mostrar_contraseña = request.GET.get('mostrar_contraseña', '')
            if mostrar_contraseña == 'si':
                usuario.password_visible = usuario.password_usuario

    return render(request, "perfil_docente.html", {'usuario': usuario, 'rol': nomUsuario.upper(), 'mostrar_contraseña': mostrar_contraseña})

#------------------------------------------------------------------------------------------------------------------------------------


def mostrarCursoDocente(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    if estadoSesion is True:
        if nomUsuario.upper() == "DOCENTE":
            cursos = Curso.objects.all()
            datos = {'nomUsuario': nomUsuario, 'cursos' : cursos} 
            return render(request, 'cursos_docente.html', datos)
        else:
            datos = {'r2': 'No Tiene Permisos Suficientes Para Acceder!!'}  
            return render(request, 'index.html', datos)
    else:
        datos = {'r2': 'Debe Iniciar Sesion Para Acceder!!'}  
        return render(request, 'index.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------

def mostrarJefaturas(request):
    jefes_cursos = Funcionario.objects.filter(jefatura_cursos__isnull=False)
    datos = {'jefes_cursos': jefes_cursos}
    return render(request, 'jefatura.html', datos)

#------------------------------------------------------------------------------------------------------------------------------------
