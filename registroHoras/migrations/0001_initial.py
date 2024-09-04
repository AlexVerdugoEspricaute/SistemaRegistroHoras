# Generated by Django 5.0.3 on 2024-05-15 21:35

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('descricion', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('centro_costo_empresa', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ClienteGrupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fecha_creacion', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='EstadoHitoCobranza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoHitoCumplimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('color', models.CharField(default='primary', max_length=30, null=True)),
                ('is_dcr_removable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Giro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField()),
                ('descripcion', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Moneda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('simbolo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ProyectoEstado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('color', models.CharField(default='primary', max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_interno', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=200)),
                ('es_asignable_en_proyecto', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TipoContrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TipoDCR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
                ('color', models.CharField(default='primary', max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoProyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AkzUsuer',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_akzio', models.BooleanField(default=True)),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='nombre de usuario')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='correo electronico')),
                ('nombre', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre')),
                ('apellido', models.CharField(blank=True, max_length=200, null=True, verbose_name='apellido')),
                ('avatar', models.ImageField(null=True, upload_to='avatars')),
                ('usuario_activo', models.BooleanField(default=True)),
                ('usuario_administrador', models.BooleanField(default=False)),
                ('Area', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='registroHoras.area')),
                ('rol', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='registroHoras.rol')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CentroCostoCliente',
            fields=[
                ('id_costo_cliente', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('nombre_costo_cliente', models.CharField(max_length=200)),
                ('tipo_servicio', models.CharField(max_length=200)),
                ('dependencia', models.CharField(max_length=200)),
                ('area_akzio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.area')),
            ],
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.ciudad')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('rut', models.CharField(max_length=50)),
                ('razon_social', models.CharField(max_length=255)),
                ('direccion', models.CharField(max_length=255)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('centro_costo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clientes', to='registroHoras.centrocostocliente')),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.ciudad')),
                ('clientegrupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.clientegrupo')),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.comuna')),
                ('giro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.giro')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=20, null=True)),
                ('email', models.CharField(max_length=50, null=True)),
                ('rut', models.CharField(max_length=50, null=True)),
                ('cliente_grupo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registroHoras.clientegrupo')),
                ('rol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registroHoras.rol')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalEmpresa',
            fields=[
                ('numero_ficha', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('rut', models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(message='El RUT debe tener un formato válido (ej: 12345678-9).', regex='^[0-9]{7,8}-[0-kK]{1}$')])),
                ('nombre', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre')),
                ('apellido', models.CharField(blank=True, max_length=200, null=True, verbose_name='apellido')),
                ('cod_cliente', models.CharField(max_length=200)),
                ('ccosto_persona', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200, unique=True, verbose_name='correo electronico')),
                ('cargo', models.CharField(max_length=100)),
                ('vigencia', models.CharField(max_length=10)),
                ('actividad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registroHoras.actividad')),
                ('ingreso_hora', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingreso_hora_personal', to=settings.AUTH_USER_MODEL)),
                ('jefatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jefatura_personal', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_redmine', models.IntegerField(blank=True, null=True)),
                ('nombre', models.CharField(max_length=255)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=23)),
                ('monto_dcr', models.DecimalField(decimal_places=2, default=0, max_digits=23)),
                ('monto_hitos_asignados', models.DecimalField(decimal_places=2, default=0, max_digits=23)),
                ('monto_hitos_facturados', models.DecimalField(decimal_places=2, default=0, max_digits=23)),
                ('hh_ofertado', models.DecimalField(decimal_places=2, max_digits=23)),
                ('fecha_inicio', models.DateField()),
                ('fecha_termino', models.DateField()),
                ('fecha_actualizacion', models.DateTimeField()),
                ('ano_actualizacion', models.CharField(max_length=4)),
                ('mes_actualizacion', models.CharField(max_length=64)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('ano_creacion', models.CharField(max_length=4)),
                ('mes_creacion', models.CharField(max_length=64)),
                ('fecha_adjudicacion', models.DateField(blank=True, null=True)),
                ('ano_adjudicacion', models.CharField(max_length=4)),
                ('mes_adjudicacion', models.CharField(blank=True, max_length=67, null=True)),
                ('fecha_envio', models.DateField(blank=True, null=True)),
                ('total_hitos', models.IntegerField(null=True)),
                ('adjuntos', models.FileField(blank=True, null=True, upload_to='adjuntos/')),
                ('observaciones', models.TextField(null=True)),
                ('asignado_a', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asignado_a', to=settings.AUTH_USER_MODEL)),
                ('autor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='autor', to='registroHoras.personalempresa')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.cliente')),
                ('cliente_pmo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente_pmo', to='registroHoras.persona')),
                ('contraparte', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contraparte', to='registroHoras.persona')),
                ('moneda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.moneda')),
                ('responsable_diseno_desarrollo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsable_diseno_desarrollo', to='registroHoras.personalempresa')),
                ('estado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registroHoras.proyectoestado')),
                ('tipo_contrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.tipocontrato')),
                ('tipo_proyecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registroHoras.tipoproyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Hito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_hito', models.IntegerField(default=0)),
                ('nombre_hito', models.CharField(max_length=100)),
                ('monto_hito', models.DecimalField(decimal_places=2, max_digits=23)),
                ('fecha_estado', models.DateTimeField(null=True)),
                ('fecha_comercial', models.DateField()),
                ('fecha_proyecto', models.DateField(null=True)),
                ('fecha_contraparte', models.DateField(null=True)),
                ('monto_asignado', models.DecimalField(decimal_places=2, default=0, max_digits=23, null=True)),
                ('monto_facturado', models.DecimalField(decimal_places=2, default=0, max_digits=23, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.estadohitocumplimiento')),
                ('estado_cobranza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.estadohitocobranza')),
                ('moneda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.moneda')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='RegistroHH',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('fecha_termino', models.DateField(blank=True, null=True)),
                ('horas_normales', models.IntegerField(null=True)),
                ('horas_extras', models.IntegerField(null=True)),
                ('horas_vacaciones', models.IntegerField(null=True)),
                ('horas_licencia', models.IntegerField(null=True)),
                ('horas_permiso', models.IntegerField(null=True)),
                ('observaciones', models.CharField(max_length=200, null=True)),
                ('seleccionar', models.BooleanField(default=False, null=True)),
                ('actividad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registroHoras.actividad')),
                ('id_hito', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registroHoras.hito')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.personalempresa')),
            ],
        ),
        migrations.CreateModel(
            name='SubArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('centro_costo_empresa', models.CharField(max_length=250)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.area')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.tipoproyecto')),
            ],
        ),
        migrations.AddField(
            model_name='personalempresa',
            name='sub_area',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='registroHoras.subarea'),
        ),
        migrations.CreateModel(
            name='ServicioCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('centro_costo_cliente', models.CharField(max_length=255)),
                ('nombre_costo_cliente', models.CharField(max_length=255)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.cliente')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registroHoras.tipoproyecto')),
            ],
        ),
    ]