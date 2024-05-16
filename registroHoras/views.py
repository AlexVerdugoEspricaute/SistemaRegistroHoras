from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import  *
from .models import RegistroHH, PersonalEmpresa
import pandas as pd
from django.utils import timezone
from django.db.models import Sum, Q, F
import datetime
from datetime import timedelta



@login_required
def register_user(request):
    if request.method == 'POST':
        form = AkzUsuerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirige a la página de inicio de sesión después de registrar exitosamente
            return redirect('panel')  
    else:
        form = AkzUsuerRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        # Si el método de la solicitud es POST, procesar el formulario de inicio de sesión
        form = LoginForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, obtener los datos limpios del formulario
            cd = form.cleaned_data
            # Autenticar al usuario utilizando las credenciales proporcionadas
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    # Si el usuario está activo, iniciar sesión y redirigir al perfil del usuario
                    login(request, user)
                    return redirect('perfil')
                else:
                    # Si el usuario no está activo, mostrar un mensaje de error
                    messages.error(request, 'El usuario no está activo')
            else:
                # Si las credenciales son incorrectas, mostrar un mensaje de error
                messages.error(request, 'Las credenciales ingresadas son incorrectas')
        else:
            # Si el formulario no es válido, mostrar un mensaje de error
            messages.error(request, 'Por favor, corrija los errores en el formulario')
    else:
        # Si el método de la solicitud no es POST, mostrar el formulario de inicio de sesión vacío
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})



@login_required
def panel(request):
    if request.user.usuario_administrador:
        # Si el usuario es un administrador, filtrar los registros por su jefatura
        jefatura_usuario = request.user
        registros_semana_actual = RegistroHH.objects.filter(persona__jefatura=jefatura_usuario)
    else:
        # Si el usuario no es administrador, filtrar los registros por su ingreso_hora
        ingreso_hora_usuario = request.user
        registros_semana_actual = RegistroHH.objects.filter(persona__ingreso_hora=ingreso_hora_usuario)

    # Resumen de todas las horas trabajadas esta semana
    horas_trabajadas_semana_actual = registros_semana_actual.aggregate(
        horas_normales=Sum('horas_normales'),
        horas_extras=Sum('horas_extras'),
        horas_vacaciones=Sum('horas_vacaciones'),
        horas_licencia=Sum('horas_licencia'),
        horas_permiso=Sum('horas_permiso'),
    )
    
    # Empleado que ha trabajado menos esta semana
    menos_trabajo = registros_semana_actual.values(
        'persona__nombre'
    ).annotate(
        total_horas= Sum('horas_normales') + Sum('horas_extras')
    ).order_by('total_horas').first()
    
    # Empleado que ha trabajado más esta semana
    mas_trabajo = registros_semana_actual.values(
        'persona__nombre'
    ).annotate(
        total_horas=Sum(F('horas_normales') + F('horas_extras'))
    ).order_by('-total_horas').first()

    context = {
        'horas_normales_semana_actual': horas_trabajadas_semana_actual.get('horas_normales', 0),
        'horas_extras_semana_actual': horas_trabajadas_semana_actual.get('horas_extras', 0),
        'horas_vacaciones_semana_actual': horas_trabajadas_semana_actual.get('horas_vacaciones', 0),
        'horas_licencia_semana_actual': horas_trabajadas_semana_actual.get('horas_licencia', 0),
        'horas_permiso_semana_actual': horas_trabajadas_semana_actual.get('horas_permiso', 0),
        'menos_trabajo': menos_trabajo['total_horas'] if menos_trabajo else 0,
        'mas_trabajo': mas_trabajo['total_horas'] if mas_trabajo else 0,
        'nombre_menos_trabajo': f"{menos_trabajo['persona__nombre']} - {menos_trabajo['total_horas']} horas." if menos_trabajo else None,
        'nombre_mas_trabajo': f"{mas_trabajo['persona__nombre']} - {mas_trabajo['total_horas']} horas." if mas_trabajo else None,
    }

    return render(request, 'account/panel.html', context)




@login_required
def visualizar(request):
    if request.method == 'POST':
        registro_id = request.POST.get('registro_id')
        registro = get_object_or_404(RegistroHH, id=registro_id)
        registro.seleccionar = not registro.seleccionar  # Invierte el estado del checkbox
        registro.save()
        return redirect('visualizar')
    else:
        form = RegistroHorasForm()

    if request.user.usuario_administrador:
        # Filtrar los registros por la jefatura del usuario administrador
        jefatura_usuario = request.user
        registros = RegistroHH.objects.filter(persona__jefatura=jefatura_usuario)
    else:
        # Filtrar los registros por el campo ingreso_hora del usuario actual
        registros = RegistroHH.objects.filter(persona__ingreso_hora=request.user)

    return render(request, 'account/visualizar.html', {'form': form, 'registros': registros})



@login_required
def password_change(request):
    return render(request, 'account/password_change.html')



@login_required
def registrar(request):
    # Obtener la jefatura del usuario logeado
    jefatura_usuario = request.user

    if request.user.usuario_administrador:
        # Si el usuario es un administrador, permitir registrar para todas las personas bajo su jefatura
        personas = PersonalEmpresa.objects.filter(jefatura=jefatura_usuario)
    else:
        # Filtrar las personas por ingreso_hora del usuario actual
        personas = PersonalEmpresa.objects.filter(ingreso_hora=request.user)
        
    # Filtrar los proyectos asignados al usuario actual
    proyectos_asignados = Proyecto.objects.filter(asignado_a=request.user)
    
    # Filtrar los hitos según los proyectos asignados al usuario actual
    hitos = Hito.objects.filter(proyecto__in=proyectos_asignados)

    if request.method == 'POST':
        form = RegistroHorasForm(request.POST, user=request.user, jefatura=jefatura_usuario)
        if form.is_valid():
            form.save()
            return redirect('visualizar')  
    else:
        if request.user.usuario_administrador:
            form = RegistroHorasForm(user=request.user, jefatura=jefatura_usuario)
        else:
            form = RegistroHorasForm(user=request.user)

    return render(request, 'account/registrar.html', {'form': form, 'personas': personas, 'hitos': hitos})



@login_required
def registrar_especial(request):
    jefatura_usuario = request.user

    if request.user.usuario_administrador:
        # Si el usuario es un administrador, permitir registrar para todas las personas bajo su jefatura
        personas = PersonalEmpresa.objects.filter(jefatura=jefatura_usuario)
    else:
        # Filtrar las personas por ingreso_hora del usuario actual
        personas = PersonalEmpresa.objects.filter(ingreso_hora=request.user)
        
    
    if request.method == 'POST':
        # Si la solicitud es POST, procesar los datos del formulario
        form = RegistroHorasEspecialesForm(request.POST)
        
        # Validar el formulario
        if form.is_valid():
            # Guardar los datos del formulario en la base de datos
            registro = form.save(commit=False)
            registro.save()
            
            # Mostrar un mensaje de éxito y redirigir a la página de visualización
            messages.success(request, "Registros exitosos: Las horas se han registrado correctamente.")
            return redirect('visualizar')  
        else:
            # Si el formulario no es válido, mostrar un mensaje de error
            messages.error(request, "Error en el formulario: Por favor, corrija los errores.")
            return render(request, 'account/registrar_especial.html', {'form': form, 'personas': personas})
    else:
        # Si la solicitud no es POST, mostrar el formulario vacío
        form = RegistroHorasEspecialesForm()
        
    # Pasar el queryset de personas al formulario para aplicar el filtro
    form.fields['persona'].queryset = personas
        
    
    return render(request, 'account/registrar_especial.html', {'form': form, 'personas': personas})


#documento del mes para softland
@login_required
def reporte_softland(request):
    # Obtener la fecha actual
    today = datetime.date.today()
    # Obtener el mes y año actuales
    current_month = today.month
    current_year = today.year

    # Obtener el nombre del mes en inglés
    month_name_english = today.strftime('%B')
    # Obtener el nombre del mes en español
    month_name_spanish = meses_en_espanol.get(month_name_english, "")

    # Filtrar los registros por mes y año actuales, y seleccionar los campos relacionados
    registros = RegistroHH.objects.filter(fecha__month=current_month, fecha__year=current_year).select_related('persona', 'id_hito__proyecto')

    # Inicializar una lista para almacenar los registros
    registros_list = []

    # Iterar sobre los registros obtenidos
    for registro in registros:
        # Calcular el total de horas para cada registro
        total_horas = (registro.horas_normales or 0) + (registro.horas_extras or 0) + (registro.horas_vacaciones or 0) + (registro.horas_licencia or 0) + (registro.horas_permiso or 0)
        # Calcular el porcentaje trabajado
        porcentaje_trabajado = f"{100 if total_horas > 0 else 0}%"
        # Agregar los datos del registro a la lista de registros
        registros_list.append({
            'Número de Documento': registro.persona.numero_ficha,
            'Centro de costo': registro.persona.ccosto_persona,
            'Porcentaje Trabajado': porcentaje_trabajado
        })

    # Crear un DataFrame a partir de la lista de registros
    df = pd.DataFrame(registros_list)

    # Crear el nombre del archivo con el nombre del mes en español y el año actual
    file_name = f"Registro de horas {month_name_spanish} {current_year}.xlsx"

    # Escribir el DataFrame en un archivo Excel
    excel_writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df.to_excel(excel_writer, index=False)
    excel_writer._save()

    # Leer el archivo Excel y configurar la respuesta HTTP
    with open(file_name, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename={file_name}'

    return response




@login_required
def exporte_a_excel_completo(request):
    # Obtener todos los registros
    registros = RegistroHH.objects.all()

    # Crear una lista de diccionarios con los datos de los registros
    datos = []
    for registro in registros:
        # Calcular el total de horas sumando todas las horas de la fila
        total_horas = sum(
            valor for valor in [
                registro.horas_normales,
                registro.horas_extras,
                registro.horas_vacaciones,
                registro.horas_licencia,
                registro.horas_permiso
            ] if valor is not None  # Filtrar valores None
        )

        datos.append({
            'Nombres': f"{registro.persona.nombre} {registro.persona.apellido}",
            'Proyectos': registro.id_hito.proyecto.id_redmine if registro.id_hito else None,
            'Nombres del Proyectos': registro.id_hito.proyecto.nombre if registro.id_hito else None,
            'Hitos': registro.id_hito.numero_hito if registro.id_hito else None,
            'Nombres Hitos': registro.id_hito.nombre_hito if registro.id_hito else None,
            'Fecha': registro.fecha,
            'Fecha inicio': registro.fecha_inicio,
            'Fecha termino': registro.fecha_termino,
            'Horas Normales': registro.horas_normales,
            'Horas Extras': registro.horas_extras,
            'Horas Vacaciones': registro.horas_vacaciones,
            'Horas Licencia': registro.horas_licencia,
            'Horas Permisos': registro.horas_permiso,
            'Total Horas': total_horas,  # Agregar el total de horas
            'Observaciones': registro.observaciones,
        })

    # Crear un DataFrame a partir de los datos
    df = pd.DataFrame(datos)

    # Crear el archivo Excel
    excel_file = df.to_excel("registros.xlsx", index=False)

    # Abrir el archivo Excel y enviarlo como una respuesta HTTP
    with open("registros.xlsx", "rb") as excel:
        response = HttpResponse(excel.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=registros.xlsx'
        return response



@login_required
def reporte_mensual(request):
    # Obtener la fecha actual
    fecha_actual = datetime.date.today()

    # Obtener el primer día del mes
    primer_dia_mes = fecha_actual.replace(day=1)

    # Obtener el último día del mes
    ultimo_dia_mes = primer_dia_mes.replace(
        day=1,
        month=primer_dia_mes.month % 12 + 1,
    ) - datetime.timedelta(days=1)

    # Filtrar los registros para el mes actual
    registros = RegistroHH.objects.filter(
        Q(fecha__gte=primer_dia_mes, fecha__lte=ultimo_dia_mes) |
        Q(fecha_inicio__lte=ultimo_dia_mes, fecha_termino__gte=primer_dia_mes)
    )

    # Inicializar una lista para almacenar los datos de la tabla
    datos_tabla = []

    # Iterar sobre los registros
    for registro in registros:
        # Calcular el total de horas para cada registro
        total_horas = (registro.horas_normales or 0) + (registro.horas_extras or 0) + (registro.horas_vacaciones or 0) + (registro.horas_licencia or 0) + (registro.horas_permiso or 0)
        # Agregar los datos a la lista de datos de la tabla
        datos_tabla.append({
            'Nombre completo': f"{registro.persona.nombre} {registro.persona.apellido}",
            'Proyecto': registro.id_hito.proyecto.nombre if registro.id_hito else None,
            'Fechas': registro.fecha,
            'Fechas inicio': registro.fecha_inicio,
            'Fechas termino': registro.fecha_termino,
            'Hrs Normales': registro.horas_normales,
            'Hrs Extras': registro.horas_extras,
            'Hrs Vacaciones': registro.horas_vacaciones,
            'Hrs Licencias': registro.horas_licencia,
            'Hrs Permisos': registro.horas_permiso,
            'Total de Horas': total_horas,
            'Observaciones': registro.observaciones,
        })

    # Crear un DataFrame a partir de los datos de la tabla
    df = pd.DataFrame(datos_tabla)

    # Traducir el nombre del mes a español
    nombre_mes_espanol = meses_en_espanol[fecha_actual.strftime('%B')]

    # Nombre del archivo con el nombre del mes y año actual en español
    nombre_archivo = f'Reporte mensual {nombre_mes_espanol} {fecha_actual.year}.xlsx'

    # Configurar la respuesta HTTP con el tipo de contenido y el nombre del archivo
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename={nombre_archivo}'

    # Escribir el DataFrame en un archivo Excel y devolver la respuesta
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return response



@login_required
def reporte_semanal(request):
    # Obtener la fecha actual
    fecha_actual = datetime.date.today()

    # Calcular el primer día de la semana
    primer_dia_semana = fecha_actual - datetime.timedelta(days=fecha_actual.weekday())

    # Calcular el último día de la semana
    ultimo_dia_semana = primer_dia_semana + datetime.timedelta(days=6)

    # Filtrar los registros para la semana actual
    registros = RegistroHH.objects.filter(
        Q(fecha_inicio__lte=ultimo_dia_semana, fecha_termino__gte=primer_dia_semana) |
        Q(fecha__gte=primer_dia_semana, fecha__lte=ultimo_dia_semana)
    )

    # Inicializar una lista para almacenar los datos de la tabla
    datos_tabla = []

    # Agrupar los registros por nombre completo de la persona y centro de costo del proyecto
    registros_agrupados = registros.values('persona__nombre', 'persona__apellido', 'id_hito__proyecto', 'actividad').annotate(
        horas_normales=Sum('horas_normales'),
        horas_extras=Sum('horas_extras'),
        horas_vacaciones=Sum('horas_vacaciones'),
        horas_licencia=Sum('horas_licencia'),
        horas_permiso=Sum('horas_permiso'),
    )

    # Iterar sobre los registros agrupados
    for registro in registros_agrupados:
        # Calcular el total de horas para cada registro
        total_horas = (registro['horas_normales'] or 0) + (registro['horas_extras'] or 0) + (registro['horas_vacaciones'] or 0) + (registro['horas_licencia'] or 0) + (registro['horas_permiso'] or 0)
        # Obtener el nombre completo
        nombre_completo = registro.get('persona__nombre', '') + ' ' + registro.get('persona__apellido', '')
        # Agregar los datos a la lista de datos de la tabla
        datos_tabla.append({
            'Nombre completo': nombre_completo,
            'Proyecto': registro['id_hito__proyecto'],
            'Actividad': registro['actividad'],
            'Hrs Normales': registro['horas_normales'],
            'Hrs Extras': registro['horas_extras'],
            'Hrs Vacaciones': registro['horas_vacaciones'],
            'Hrs Licencias': registro['horas_licencia'],
            'Hrs Permisos': registro['horas_permiso'],
            'Total de Horas': total_horas,
        })

    # Crear un DataFrame a partir de los datos de la tabla
    df = pd.DataFrame(datos_tabla)

    # Crear el nombre del archivo para el reporte
    nombre_archivo = f'Reporte semana {primer_dia_semana.strftime("%d-%m-%Y")} al {ultimo_dia_semana.strftime("%d-%m-%Y")}.xlsx'

    # Configurar la respuesta HTTP con el tipo de contenido y el nombre del archivo
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename={nombre_archivo}'

    # Escribir el DataFrame en un archivo Excel y devolver la respuesta
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return response