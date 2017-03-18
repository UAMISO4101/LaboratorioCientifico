# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-18 21:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio', '0002_auto_20170317_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransaccionInventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField()),
                ('fecha_ejecucion', models.DateTimeField()),
                ('nivel_origen', models.IntegerField(null=True)),
                ('seccion_origen', models.IntegerField(null=True)),
                ('nivel_destino', models.IntegerField(null=True)),
                ('seccion_destino', models.IntegerField(null=True)),
                ('cantidad', models.IntegerField(null=True)),
                ('comentarios', models.CharField(max_length=200, null=True)),
                ('autoriza', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='autorizaTrx', to=settings.AUTH_USER_MODEL)),
                ('bodega_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bodegaDestino', to='laboratorio.Bodega')),
                ('bodega_origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bodegaOrigen', to='laboratorio.Bodega')),
                ('estado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tipo_estado', to='laboratorio.Tipo')),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratorio.Producto')),
                ('producto_bodega_destino', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ubucacionDestino', to='laboratorio.ProductosEnBodega')),
                ('producto_bodega_origen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ubucacionOrigen', to='laboratorio.ProductosEnBodega')),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tipo_trx', to='laboratorio.Tipo')),
                ('unidad_medida', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tipo_unidadmedida', to='laboratorio.Tipo')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarioTrx', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
