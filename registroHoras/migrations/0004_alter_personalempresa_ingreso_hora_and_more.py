# Generated by Django 5.0.3 on 2024-05-15 22:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registroHoras', '0003_alter_proyecto_cliente_pmo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalempresa',
            name='ingreso_hora',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingreso_hora', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='personalempresa',
            name='jefatura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jefatura', to=settings.AUTH_USER_MODEL),
        ),
    ]