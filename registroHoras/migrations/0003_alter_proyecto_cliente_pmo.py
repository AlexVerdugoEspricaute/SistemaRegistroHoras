# Generated by Django 5.0.3 on 2024-05-15 21:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registroHoras', '0002_alter_proyecto_contraparte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='cliente_pmo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente_pmo', to='registroHoras.cliente'),
        ),
    ]
