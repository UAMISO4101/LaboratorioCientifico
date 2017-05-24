# coding=utf-8

import json
import time
import sys
from django.utils import timezone
from django.core import serializers
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from laboratorio.models import Ajuste, DetalleProductos, Tipo, TransaccionInventario, Bodega, Usuario
from django.shortcuts import render
from .views_transacciones import ejecutar_transaccion
from laboratorio.modelos_vista import AjusteVista, Convertidor


"""
Views para manejo de ajustes creados
"""


"""Metodo para navegar proceso de aprobacion de ajustes.
"""
def ir_aprobacion_ajuste(request):
    return render(request, "laboratorio/ver_ajustes.html")


"""Metodo para obtener ajustes por aprobar.
HU: DA-LCINV-10: Cientifico lider aprueba ajustes
Sirve para obtener los ajustes disponibles para aprobar
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtener_ajustes(request):
    qs = Ajuste.objects.all()
    listaA = []
    for ajuste_n in qs:
        ajuste = AjusteVista()
        ajuste.id = ajuste_n.id
        ajuste.producto = ajuste_n.producto.nombre
        ajuste.bodega = ajuste_n.bodega.nombre
        ajuste.tipo_diferencia = ajuste_n.tipo_diferencia.nombre
        ajuste.diferencia_cantidad = ajuste_n.diferencia_cantidad
        ajuste.estado = ajuste_n.estado.nombre
        listaA.append(ajuste)
    json_string = json.dumps(listaA, cls=Convertidor)
    return JsonResponse(json_string, safe=False)

"""Metodo aprobar un ajuste.
HU: DA-LCINV-18: Cientifico lider aprueba un ajuste
Sirve para aprobar un ajuste de inventario
request, es la peticion dada por el usuario
return, formato json con mensaje de confirmación
"""
@csrf_exempt
def aprobar_ajuste(request):
    ajuste = Ajuste.objects.get(id=request.POST['id_a'])
    ajuste.detalle_productos.unidad_medida
    if ajuste.estado.nombre =="En aprobacion" and ajuste.estado.grupo == "AJUSTE":
        if ajuste.tipo_diferencia.nombre == "Exceso":
            transaccion = transaccion_por_exceso(ajuste)
        elif ajuste.tipo_diferencia.nombre == "Defecto":
            transaccion = transaccion_por_defecto(ajuste)
        # Ejecuta la transaccion (movimiento entre bodegas)
        ejecutar_transaccion(transaccion, request)
        ajuste.transaccion_inventario=transaccion
        ajuste.estado = Tipo.objects.get(nombre="Aprobada", grupo="AJUSTE")
        ajuste.save()
        return JsonResponse({"mensaje": 'ok'})
    else:
        return JsonResponse({"mensaje": 'La aprobación no puede ser realizada'})

"""Metodo auxiliar para ajustes por exceso.
HU: DA-LCINV-18: Cientifico lider aprueba un ajuste
Sirve para crear la transaccion por exceso de inventario
request, es la peticion dada por el usuario
return, formato json con mensaje de confirmación
"""
def transaccion_por_exceso(ajuste):
    desperdicio = Tipo.objects.filter(nombre="Desperdicio").first()
    transaccion = TransaccionInventario(
        tipo=Tipo.objects.get(nombre='Ajuste Inventario', grupo='TIPOTRX'),
        bodega_origen=Bodega.objects.get(pk=ajuste.bodega_id),
        producto_bodega_origen=ajuste.detalle_productos.productosenbodega,
        nivel_origen=ajuste.nivel,
        seccion_origen=ajuste.seccion,
        bodega_destino=Bodega.objects.filter(tipo_bodega=desperdicio).first(),
        nivel_destino=1,
        seccion_destino =1,
        producto = ajuste.producto,
        cantidad = ajuste.diferencia_cantidad,
        unidad_medida = ajuste.detalle_productos.unidad_medida,
        estado = Tipo.objects.get(pk=Tipo.objects.filter(nombre='Ejecutada', grupo='STATUSTRX').first().id),
        fecha_creacion = timezone.now(),
        fecha_ejecucion = timezone.now(),
        usuario = Usuario.objects.get(pk=1),
        comentarios = 'Transacción Automática Ajuste No' + str(ajuste.id)
    )
    transaccion.save()
    return transaccion

"""Metodo auxiliar para ajustes por defecto.
HU: DA-LCINV-18: Cientifico lider aprueba un ajuste
Sirve para crear la transaccion por defecto de inventario
request, es la peticion dada por el usuario
return, formato json con mensaje de confirmación
"""
def transaccion_por_defecto(ajuste):
    externa = Tipo.objects.filter(nombre="Externa").first()
    transaccion = TransaccionInventario(
        tipo=Tipo.objects.get(nombre='Ajuste Inventario', grupo='TIPOTRX'),
        bodega_origen=Bodega.objects.get(tipo_bodega=externa),
        nivel_origen=1,
        seccion_origen=1,
        bodega_destino=Bodega.objects.filter(pk=ajuste.bodega_id).first(),
        nivel_destino=ajuste.nivel,
        seccion_destino=ajuste.seccion,
        producto=ajuste.producto,
        cantidad=ajuste.diferencia_cantidad,
        unidad_medida=ajuste.detalle_productos.unidad_medida,
        estado=Tipo.objects.get(pk=Tipo.objects.filter(nombre='Ejecutada', grupo='STATUSTRX').first().id),
        fecha_creacion=timezone.now(),
        fecha_ejecucion=timezone.now(),
        usuario=Usuario.objects.get(pk=1),
        comentarios='Transacción Automática Ajuste No' + str(ajuste.id)
    )
    transaccion.save()
    return transaccion
