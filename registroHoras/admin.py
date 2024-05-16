from django.contrib import admin
from .models import *


class AreaAdmin(admin.ModelAdmin):
    list_display = ['nombre','centro_costo_empresa']
    
    
class SubAreaAdmin(admin.ModelAdmin):
    list_display = ['nombre','centro_costo_empresa','servicio','area']


class ServicioClienteAdmin(admin.ModelAdmin):
    list_display = ['centro_costo_cliente','nombre_costo_cliente','servicio','cliente']


class PersonalEmpresaAdmin(admin.ModelAdmin):
    list_display = ['numero_ficha','rut','nombre','apellido','cod_cliente','ccosto_persona','email','ingreso_hora','jefatura','cargo','vigencia','numero_ficha','sub_area','actividad']


class CentroCostoClienteAdmin(admin.ModelAdmin):
    list_display = ['id_costo_cliente', 'nombre_costo_cliente','tipo_servicio','area_akzio','dependencia']


class AkzUsuarioAdmin(admin.ModelAdmin):
    list_display = ['id','is_akzio','username', 'email', 'nombre', 'apellido','rol','avatar','Area', 'usuario_activo', 'usuario_administrador']


class ProyectoEstadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'color']


class TipoProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre']


class GrupoClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_creacion']


class CiudadAdmin(admin.ModelAdmin):
    list_display = ['nombre']


class ComunaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad']


class EstadoHitoCumplimientoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'color', 'is_dcr_removable']


class EstadoHitoCobranzaAdmin(admin.ModelAdmin):
    list_display = ['nombre']


class GiroAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion']


class MonedaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'simbolo']


class ServicioAdmin(admin.ModelAdmin):
    list_display = ['id_servicio', 'nombre_servicio']


class TipoDCRAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'color']


class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rut', 'razon_social', 'clientegrupo', 'direccion', 'comuna', 'ciudad', 'giro', 'fecha_creacion','centro_costo']


class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre_interno', 'nombre', 'descripcion', 'es_asignable_en_proyecto']


class TipoContratoAdmin(admin.ModelAdmin):
    list_display = ['nombre']


class PersonaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'apellido', 'cliente_grupo', 'rol' , 'telefono', 'email', 'rut']


class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['id_redmine', 'nombre', 'estado', 'cliente',
                    'monto', 'monto_dcr', 'monto_hitos_asignados', 
                    'monto_hitos_facturados', 'hh_ofertado', 'moneda', 
                    'tipo_proyecto', 'tipo_contrato', 'fecha_inicio', 
                    'fecha_termino', 'fecha_actualizacion','ano_actualizacion','mes_actualizacion', 'fecha_creacion','ano_creacion','mes_creacion',
                    'fecha_adjudicacion','mes_adjudicacion', 'fecha_envio', 'autor', 'asignado_a', 'contraparte',
                    'responsable_diseno_desarrollo', 'total_hitos', 'adjuntos', 'observaciones', 'cliente_pmo']


class HitoAdmin(admin.ModelAdmin):
    list_display = ['numero_hito', 'nombre_hito', 'monto_hito', 'estado', 'estado_cobranza', 'fecha_estado',
                    'fecha_comercial', 'fecha_proyecto', 'fecha_contraparte', 
                    'proyecto', 'moneda', 'monto_asignado', 'monto_facturado', 'activo']


class RegistroHHAdmin(admin.ModelAdmin):
    list_display = ['persona', 'id_hito','actividad' , 'fecha', 
                    'fecha_inicio', 'fecha_termino', 'horas_normales', 'horas_extras', 'horas_vacaciones', 'horas_licencia', 'horas_permiso', 'observaciones','seleccionar']

class ActividadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descricion']


admin.site.register(AkzUsuer, AkzUsuarioAdmin)
admin.site.register(ServicioCliente,ServicioClienteAdmin)
admin.site.register(Area,AreaAdmin)
admin.site.register(SubArea,SubAreaAdmin)
admin.site.register(PersonalEmpresa,PersonalEmpresaAdmin)
admin.site.register(Actividad,ActividadAdmin)
admin.site.register(ProyectoEstado, ProyectoEstadoAdmin)
admin.site.register(TipoProyecto, TipoProyectoAdmin)
admin.site.register(ClienteGrupo, GrupoClienteAdmin)
admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Comuna, ComunaAdmin)
admin.site.register(EstadoHitoCumplimiento, EstadoHitoCumplimientoAdmin)
admin.site.register(EstadoHitoCobranza, EstadoHitoCobranzaAdmin)
admin.site.register(Giro, GiroAdmin)
admin.site.register(Moneda, MonedaAdmin)
admin.site.register(TipoDCR, TipoDCRAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Rol, RolAdmin)
admin.site.register(TipoContrato, TipoContratoAdmin)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Hito, HitoAdmin)
admin.site.register(RegistroHH, RegistroHHAdmin)
admin.site.register(CentroCostoCliente, CentroCostoClienteAdmin)
