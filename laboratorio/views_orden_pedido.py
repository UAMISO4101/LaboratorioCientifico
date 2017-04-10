# coding=utf-8

import decimal
import json
import time
from dateutil import tz
from datetime import datetime, timedelta

from django.utils.timezone import localtime
from operator import attrgetter

from decimal import Decimal

import sys
from django.core import serializers

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse, HttpResponse

from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from psycopg2.extensions import JSON

from laboratorio.modelos_vista import BodegaVista, Convertidor, ProductoVista, ProductosBodegaVista, RecursoBusquedaVista, RecursoBusquedaDetalleVista, TransaccionVista, json_default, \
    OrdenPedidoVista
from laboratorio.models import Tipo, Usuario, Bodega, Experimento, ProductoProtocolo, Producto, Protocolo, OrdenPedido
from laboratorio.models import TransaccionInventario, Producto, ProductosEnBodega
from laboratorio.utils.utils import utils

"""Metodo a navegar ordenes de pedido.
"""
def ir_ver_ordenes_pedido(request):
    return render(request, "laboratorio/ver_ordenes_pedido.html")

"""Metodo a navegar orden de pedido.
"""
def ir_orden_pedido(request):
    return render(request, "laboratorio/orden_pedido.html")

"""Metodo obtener los usuarios del sistema sin proveedores y sin admin.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para obtener los usuarios que existen en el sistema que no son proveedores y no admin
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtenerSoloUsuarios(request):
    qs = Usuario.objects.filter(is_superuser=False).exclude(roles__nombre = 'Proveedor')
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)


"""Metodo obtener los estados de la orden de pedido.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para obtener los estados que puede tener una orden de pedido
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtenerEstadosOP(request):
    qs = Tipo.objects.filter(grupo='ORDENPEDIDO')
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)

"""Metodo obtener fecha actual.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para obtener la fecha actual del sistema
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtener_fecha_actual(request):
    fecha_actual = time.strftime("%c")
    return JsonResponse({"fecha": fecha_actual})

"""Metodo a navegar actualizar orden de pedido.
HU: EC-LCINV-17: Crear Orden de Pedido
"""
def ir_act_orden_pedido(request):
    return render(request, "laboratorio/act_orden_pedido.html")

"""Metodo crear orden de pedido.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para crear una orden de pedido en el sistema
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def crear_orden_pedido(request):
    mensaje = ""
    if request.method == 'POST':
        orden_pedido = OrdenPedido(fecha_peticion=datetime.strptime(request.POST['fecha_creacion'], '%c'),
                        estado=Tipo.objects.filter(id=request.POST['estado']).first(),
                        usuario_creacion=Usuario.objects.filter(id=request.POST['usuario_creacion']).first(),
                        proveedor=Usuario.objects.filter(id=request.POST['proveedor']).first(),
                        observaciones=request.POST['observaciones'])

        orden_pedido.save()
        mensaje = orden_pedido.id

    return JsonResponse({"id": mensaje})

"""Metodo obtener orden de pedido.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para obtener la orden de pedido dado el id de la orden
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtener_op(request):
    time.sleep(0.3)
    qs = OrdenPedido.objects.filter(id=request.GET['id_op'])
    qs_json = serializers.serialize('json', qs)
    struct = json.loads(qs_json)
    json_op = json.dumps(struct[0])
    return JsonResponse({"op": json_op})

"""Metodo obtener orden de pedido.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para obtener la orden de pedido dado el id de la orden
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtener_fecha_peticion_op(request):
    time.sleep(0.3)
    qs = OrdenPedido.objects.filter(id=request.GET['id_op'])
    orden_pedido = qs.first()
    dh = timedelta(hours=5)
    return JsonResponse({"fecha_peticion": (orden_pedido.fecha_peticion - dh).strftime("%c")})


"""Metodo obtener ordenes de pedido.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para obtener las ordenes de pedido que tiene el sistema
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtenerOrdenesPedido(request):
    qs = OrdenPedido.objects.all()
    listaOps = []
    for orden_pedido in qs:
        orden = OrdenPedidoVista()
        orden.id = orden_pedido.id
        if orden_pedido.usuario_creacion != None:
            orden.nombreUsuarioCreacion = orden_pedido.usuario_creacion.first_name + " " + orden_pedido.usuario_creacion.last_name
        else:
            orden.nombreUsuarioCreacion = " "
        if orden_pedido.usuario_aprobacion != None:
            orden.nombreUsuarioAprobacion = orden_pedido.usuario_aprobacion.first_name + " " + orden_pedido.usuario_aprobacion.last_name
        else:
            orden.nombreUsuarioAprobacion = " "
        if orden_pedido.proveedor != None:
            orden.nombreProveedor = orden_pedido.proveedor.first_name + " " + orden_pedido.proveedor.last_name
        else:
            orden.nombreProveedor = " "
        orden.estado = orden_pedido.estado.nombre
        dh = timedelta(hours=5)
        orden.fechaPeticion = (orden_pedido.fecha_peticion - dh).strftime("%c")
        listaOps.append(orden)
    json_string = json.dumps(listaOps, cls=Convertidor)
    return JsonResponse(json_string, safe=False)