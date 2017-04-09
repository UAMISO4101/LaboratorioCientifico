# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-09 16:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio', '0004_bodega_unidad_medida'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleOrden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=8, max_digits=11, null=True)),
                ('fecha_movimiento', models.DateTimeField(null=True)),
                ('nivel_bodega_destino', models.IntegerField(null=True)),
                ('seccion_bodega_destino', models.IntegerField(null=True)),
                ('bodega', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratorio.Bodega')),
                ('estado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='do_estado', to='laboratorio.Tipo')),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratorio.Producto')),
                ('transaccion_inventario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='do_transaccion', to='laboratorio.TransaccionInventario')),
            ],
        ),
        migrations.CreateModel(
            name='OrdenPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_peticion', models.DateTimeField(null=True)),
                ('fecha_recepcion', models.DateTimeField(null=True)),
                ('observaciones', models.CharField(max_length=500)),
                ('notas_aprobacion', models.CharField(max_length=500)),
                ('estado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='op_estado', to='laboratorio.Tipo')),
                ('proveedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='op_proveedor', to=settings.AUTH_USER_MODEL)),
                ('usuario_aprobacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='op_usuario_aprobacion', to=settings.AUTH_USER_MODEL)),
                ('usuario_creacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='op_usuario_creacion', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
