
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator



# Validador para el RUT
rut_validator = RegexValidator(
    regex=r'^[0-9]{7,8}-[0-kK]{1}$',
    message='El RUT debe tener un formato válido (ej: 12345678-9).'
)


# Manejador de usuarios personalizado
class UsuarioManager(BaseUserManager):
    # Crea y guarda un usuario con los detalles proporcionados.
    def create_user(self, email, username, nombre, apellido, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')

        usuario = self.model(
            username=username, 
            email=self.normalize_email(email),
            nombre=nombre, 
            apellido=apellido
        )

        usuario.set_password(password)
        usuario.save()
        return usuario

    # Crea y guarda un superusuario con los detalles proporcionados.
    def create_superuser(self, username, email, nombre, apellido, password):
        usuario = self.create_user(
            email=email,
            username=username, 
            nombre=nombre, 
            apellido=apellido,
            password=password
        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario



class Rol(models.Model):
    nombre_interno = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    es_asignable_en_proyecto = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.nombre_interno



class TipoProyecto(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre



class Area(models.Model):
    nombre = models.CharField(max_length=255)
    centro_costo_empresa = models.CharField(max_length=250)

    def __str__(self):
        return self.nombre
    
    
    
class SubArea(models.Model):
    nombre = models.CharField(max_length=255)
    centro_costo_empresa = models.CharField(max_length=250)
    servicio = models.ForeignKey(TipoProyecto, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre



class Actividad(models.Model):
    nombre = models.CharField(max_length=250)
    descricion = models.CharField(max_length=250)


    def __str__(self):
        return self.nombre



# Modelo personalizado de usuario
class AkzUsuer(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    is_akzio = models.BooleanField(default=True)
    username = models.CharField('nombre de usuario',unique=True,max_length=100)
    email = models.EmailField('correo electronico',max_length=100, unique=True)
    nombre = models.CharField('Nombre', max_length= 200, blank= True, null= True)
    apellido = models.CharField('apellido', max_length= 200, blank= True, null= True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, default=None, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True)
    Area = models.ForeignKey(Area, on_delete=models.CASCADE, default=None, null=True, blank=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre','apellido','email']

    def __str__ (self):
        return self.email

    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property 
    def is_staff(self):
        return self.usuario_administrador


class PersonalEmpresa(models.Model):
    numero_ficha = models.CharField(max_length=100, primary_key=True, unique=True)
    rut = models.CharField(max_length=100, unique=True, validators=[rut_validator])
    nombre = models.CharField('Nombre', max_length=200, blank=True, null=True)
    apellido = models.CharField('apellido', max_length=200, blank=True, null=True)
    cod_cliente = models.CharField(max_length=200)
    ccosto_persona = models.CharField(max_length=200)
    email = models.EmailField('correo electronico', max_length=200, unique=True)
    ingreso_hora = models.ForeignKey(AkzUsuer, on_delete=models.CASCADE, related_name='ingreso_hora')
    jefatura = models.ForeignKey(AkzUsuer, on_delete=models.CASCADE, related_name='jefatura')
    cargo = models.CharField(max_length=100)
    vigencia = models.CharField(max_length=10)
    sub_area = models.ForeignKey(SubArea, on_delete=models.CASCADE, blank=True)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"



class ProyectoEstado(models.Model):
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=30, default='primary', null=True)

    def __str__(self):
        return self.nombre



class ClienteGrupo(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField()

    def __str__(self):
        return self.nombre



class Ciudad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre



class Comuna(models.Model):
    nombre = models.CharField(max_length=50)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre



class EstadoHitoCumplimiento(models.Model):
    nombre = models.CharField(max_length=30)
    color = models.CharField(max_length=30, default='primary', null=True)
    is_dcr_removable = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre



class EstadoHitoCobranza(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre



class Giro(models.Model):
    codigo = models.IntegerField()
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion



class Moneda(models.Model):
    nombre = models.CharField(max_length=50)
    simbolo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre



class TipoDCR(models.Model):
    tipo = models.CharField(max_length=50)
    color = models.CharField(max_length=30, default='primary', null=True)

    def __str__(self):
        return self.tipo


    
class CentroCostoCliente(models.Model):
    id_costo_cliente = models.CharField(max_length=50, primary_key=True, unique=True)
    nombre_costo_cliente = models.CharField(max_length=200)
    tipo_servicio = models.CharField(max_length=200)
    area_akzio = models.ForeignKey(Area, on_delete=models.CASCADE)
    dependencia = models.CharField(max_length=200)

    def __str__(self):
        return self.id_costo_cliente

class TipoContrato(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre



class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    rut = models.CharField(max_length=50)
    razon_social = models.CharField(max_length=255)
    clientegrupo = models.ForeignKey(ClienteGrupo, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE) # esto venia : ciudad = models.IntegerField()
    giro = models.ForeignKey(Giro, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    centro_costo = models.ForeignKey(CentroCostoCliente, on_delete=models.CASCADE, related_name="clientes") 

    def __str__(self):
        return self.nombre



class ServicioCliente(models.Model):
    centro_costo_cliente = models.CharField(max_length=255)
    nombre_costo_cliente = models.CharField(max_length=255)
    servicio = models.ForeignKey(TipoProyecto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre_costo_cliente



class Persona(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cliente_grupo = models.ForeignKey(ClienteGrupo, on_delete=models.CASCADE, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True)
    telefono = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True)
    rut = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.nombre



class Proyecto(models.Model):
    id_redmine = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=255)
    estado = models.ForeignKey(ProyectoEstado, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=23, decimal_places=2)
    monto_dcr = models.DecimalField(max_digits=23, decimal_places=2, default=0)
    monto_hitos_asignados = models.DecimalField(max_digits=23, decimal_places=2, default=0)
    monto_hitos_facturados = models.DecimalField(max_digits=23, decimal_places=2, default=0)
    hh_ofertado = models.DecimalField(max_digits=23, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE) 
    tipo_proyecto = models.ForeignKey(TipoProyecto, on_delete=models.CASCADE, blank=True, null=True)
    tipo_contrato = models.ForeignKey(TipoContrato, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    fecha_actualizacion = models.DateTimeField()
    ano_actualizacion = models.CharField(max_length=4)
    mes_actualizacion = models.CharField(max_length=64)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ano_creacion = models.CharField(max_length=4)
    mes_creacion = models.CharField(max_length=64)
    fecha_adjudicacion = models.DateField(null=True, blank=True)
    ano_adjudicacion = models.CharField(max_length=4)
    mes_adjudicacion = models.CharField(max_length=67, null=True, blank=True)
    fecha_envio = models.DateField(null=True, blank=True)
    autor = models.ForeignKey(PersonalEmpresa, on_delete=models.CASCADE, related_name="autor", null=True)
    asignado_a = models.ForeignKey(AkzUsuer, on_delete=models.CASCADE, related_name="asignado_a", null=True)
    contraparte = models.ForeignKey(PersonalEmpresa, on_delete=models.CASCADE, related_name="contraparte", null=True)
    responsable_diseno_desarrollo = models.ForeignKey(PersonalEmpresa, on_delete=models.CASCADE, related_name="responsable_diseno_desarrollo", blank=True, null=True)
    total_hitos = models.IntegerField(null=True)
    adjuntos = models.FileField(upload_to='adjuntos/', null=True, blank=True)
    observaciones = models.TextField(null=True)
    cliente_pmo = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="cliente_pmo", null=True)

    def __str__(self):
        return self.nombre



class Hito(models.Model):   
    numero_hito = models.IntegerField(default=0)
    nombre_hito = models.CharField(max_length=100) 
    monto_hito = models.DecimalField(max_digits=23, decimal_places=2)
    estado = models.ForeignKey(EstadoHitoCumplimiento, on_delete=models.CASCADE)
    estado_cobranza = models.ForeignKey(EstadoHitoCobranza, on_delete=models.CASCADE)
    fecha_estado = models.DateTimeField(null=True)
    fecha_comercial = models.DateField(null=False)
    fecha_proyecto = models.DateField(null=True)
    fecha_contraparte = models.DateField(null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    monto_asignado = models.DecimalField(max_digits=23, decimal_places=2, null=True, default=0)
    monto_facturado = models.DecimalField(max_digits=23, decimal_places=2, null=True, default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_hito



class RegistroHH(models.Model):
    persona = models.ForeignKey(PersonalEmpresa, on_delete=models.CASCADE)
    id_hito = models.ForeignKey(Hito, on_delete=models.CASCADE, null=True)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, null=True)
    fecha = models.DateField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_termino = models.DateField(null=True, blank=True)
    horas_normales = models.IntegerField(null=True)
    horas_extras = models.IntegerField(null=True)
    horas_vacaciones = models.IntegerField(null=True)
    horas_licencia = models.IntegerField(null=True)
    horas_permiso = models.IntegerField(null=True)
    observaciones = models.CharField(max_length=200, null=True)
    seleccionar = models.BooleanField(default=False, null=True)



# class DCR(models.Model):
#     numero_dcr = models.CharField(max_length=50)
#     estado = models.ForeignKey(EstadoDCR, on_delete=models.CASCADE)
#     fecha_estado = models.DateTimeField(null=True)
#     grupo_cliente = models.ForeignKey(ClienteGrupo, on_delete=models.CASCADE)
#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
#     tipo = models.ForeignKey(TipoDCR, on_delete=models.CASCADE)
#     moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
#     monto = models.DecimalField(max_digits=23, decimal_places=2, null=True)
#     monto_consumido_proyecto = models.DecimalField(max_digits=23, decimal_places=2, default=0, null=True )
#     monto_consumido_hito = models.DecimalField(max_digits=23, decimal_places=2, default=0, null=True  )
#     monto_disponible_proyecto = models.DecimalField(max_digits=23, decimal_places=2, default=0, null=True)
#     monto_disponible_hito = models.DecimalField(max_digits=23, decimal_places=2, default=0, null=True)
#     monto_facturado = models.DecimalField(max_digits=23, decimal_places=2, default=0, null=True)
#     total_proyecto = models.IntegerField(null=True)
#     total_hitos = models.IntegerField(null=True)
#     observacion = models.TextField(null=True)
#     proyecto = models.ManyToManyField(Proyecto, through='ProyectoDCR')

#     def __str__(self):
#         return self.numero_dcr



# class ProyectosDCR(models.Model):
#     proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
#     dcr = models.ForeignKey(DCR, on_delete=models.CASCADE)
#     monto_asignacion = models.DecimalField(max_digits=23, decimal_places=2, default=0, null=True, blank=True)
#     monto_consumido = models.DecimalField(max_digits=23, decimal_places=2, default=0, null=True, blank=True)
#     monto_disponible = models.DecimalField(max_digits=23, decimal_places=2, default=0, null=True, blank=True)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_actualizacion = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ('proyecto', 'dcr')



# class ProyectosDCRHitos(models.Model):
#     proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
#     dcr = models.ForeignKey(DCR, on_delete=models.CASCADE)
#     hito = models.ForeignKey(Hito, on_delete=models.CASCADE)
#     proyecto_dcr = models.ForeignKey(ProyectosDCR, on_delete=models.CASCADE)
#     monto_asignacion = models.DecimalField(max_digits=23, decimal_places=2, default=0, null=True, blank=True )
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_actualizacion = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ('proyecto_dcr', 'hito')



# class Param(models.Model):
#     nombre_interno = models.CharField(max_length=50, unique=True)
#     descripcion = models.CharField(max_length=255, null=True)

#     def __str__(self):
#         return self.nombre_interno



# class LogHito(models.Model):
#     usuario = models.ForeignKey(AkzUsuer, on_delete=models.CASCADE)
#     hito = models.ForeignKey(Hito, on_delete=models.CASCADE)
#     proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
#     tipo = models.CharField(max_length=50)
#     param = models.ForeignKey(Param, on_delete=models.CASCADE, null=True)
#     descripcion = models.TextField(null=True)
#     fecha_creacion = models.DateTimeField()
#     comentario = models.TextField(null=True)

#     def __str__(self):
#         return self.hito


# class AccionPermitida(models.Model):
#     nombre = models.CharField(max_length=250)
#     nombre_interno = models.CharField(max_length=250)

#     def __str__(self):
#         return self.nombre


# class EstadoFlujoHitoCumplimiento(models.Model):
#     rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
#     estado_actual = models.ForeignKey(EstadoHitoCumplimiento, on_delete=models.CASCADE)
#     estado_proximo = models.ForeignKey(EstadoHitoCumplimiento, on_delete=models.CASCADE,
#                                     related_name="estados_proximos")
#     accion_permitida = models.ForeignKey(AccionPermitida, on_delete=models.CASCADE)
#     activo = models.BooleanField(default=True)



# class LogDCR(models.Model):
#     usuario = models.ForeignKey(AkzUsuer, on_delete=models.CASCADE)
#     action = models.CharField(max_length=50, null=True)
#     descripcion = models.TextField(null=True)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     id_dcr = models.CharField(max_length=50, null=True)



# class ParamProyecto(models.Model):
#     nombre_interno = models.CharField(max_length=50, unique=True)
#     descripcion = models.CharField(max_length=255, null=True)



# class LogProyecto(models.Model):
#     usuario = models.ForeignKey(AkzUsuer, on_delete=models.CASCADE)
#     proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
#     param = models.ForeignKey(ParamProyecto, on_delete=models.CASCADE, null=True)
#     descripcion = models.TextField(null=True)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)


# class ProyectoFavorito(models.Model):
#     usuario = models.ForeignKey(AkzUsuer, on_delete=models.CASCADE)
#     proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)


# class TipoNotificacion(models.Model):
#     tipo = models.CharField(max_length=50)

#     def __str__(self):
#         return self.tipo


# class Link(models.Model):
#     url = models.CharField(max_length=100, default='#') 

#     def __str__(self):
#         return self.url


# class Mensaje(models.Model):
#     nombre_interno = models.CharField(max_length=50, unique=True)
#     mensaje = models.CharField(max_length=250)

#     def __str__(self):
#         return self.mensaje


# class PlantillaHTML(models.Model):
#     nombre_interno = models.CharField(max_length=50, unique=True)
#     plantilla = models.CharField(max_length=250)

#     def __str__(self):
#         return self.nombre_interno

# class Evento(models.Model):
#     nombre = models.CharField(max_length=250, default='default')
#     parametro = models.OneToOneField(Mensaje, on_delete=models.CASCADE)
#     plantilla_url = models.ForeignKey(Link, on_delete=models.CASCADE)
#     descripcion = models.TextField(default=None)

#     def __str__(self):
#         return self.nombre


# class Suscripcion(models.Model):
#     usuario = models.OneToOneField(AkzUsuer, on_delete=models.CASCADE)
#     evento = models.ManyToManyField(Evento, through='SendToNotificaciones')


# class EnviarNotificacion(models.Model):
#     suscripcion = models.ForeignKey(Suscripcion, on_delete=models.CASCADE)
#     eventos = models.ForeignKey(Evento, on_delete=models.CASCADE)
#     enviar_correo = models.BooleanField(default=False)
#     enviar_web = models.BooleanField(default=True) 


# class Notificacion(models.Model):
#     usuario_emisor = models.ForeignKey(AkzUsuer, on_delete=models.CASCADE)
#     usuario_receptor = models.ManyToManyField(AkzUsuer, related_name='receptores', through='NotificacionVista')
#     url = models.CharField(max_length=100, default='#') #si crearon una tabla porque no lo llaman por clave foranea? 
#     mensaje = models.TextField()
#     fecha_creacion = models.DateTimeField(auto_now_add=True)



# class NotificacionVista(models.Model):
#     notificacion = models.ForeignKey(Notificacion, on_delete=models.CASCADE)
#     akz_usuario = models.ForeignKey(AkzUsuer, on_delete=models.CASCADE) 
#     visto = models.BooleanField(default=False)

#     class Meta:
#         unique_together = ('notificacion', 'akz_usuario')



# class RemoverContenido(models.Model):
#     info = models.CharField(max_length=100)
#     rol = models.ManyToManyField(Rol)



# class NotificacionPorDefecto(models.Model):
#     rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
#     evento = models.ManyToManyField(Evento)






