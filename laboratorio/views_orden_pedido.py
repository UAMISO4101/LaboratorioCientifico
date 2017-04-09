# coding=utf-8

import decimal
import json
import time
from datetime import datetime
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

from laboratorio.modelos_vista import BodegaVista, Convertidor, ProductoVista, ProductosBodegaVista, RecursoBusquedaVista, RecursoBusquedaDetalleVista, TransaccionVista, json_default
from laboratorio.models import Tipo, Usuario, Bodega, Experimento, ProductoProtocolo, Producto, Protocolo
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