# Generated by Django 5.0.3 on 2024-05-15 21:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registroHoras', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='contraparte',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contraparte', to='registroHoras.personalempresa'),
        ),
    ]
