# coding=utf-8

import json
import time
import sys
from django.core import serializers
from datetime import datetime, timedelta
from decimal import Decimal
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from laboratorio import views_nivel_insumos
from laboratorio.modelos_vista import BodegaVista, Convertidor, TransaccionVista, json_default
from laboratorio.models import Ajuste, DetalleProductos
from laboratorio.models import Tipo, Usuario, Bodega, TransaccionInventario, ProductosEnBodega, Producto
from django.shortcuts import render


'''
Recibe el numero de conteo de inventario
Selecciona todos los registros de dicho conteo que tengan una diferencia entre lo contado automatica y fisicamente
Por cada uno de los registros se inserta un regristo en la tabla de ajustes
'''

@csrf_exempt
def generarAjustesConteo(request):
    conteoInvId = request.GET['id_conteo']
    qs = DetalleProductos.objects.filter(conteoinventario=conteoInvId).exclude(diferencia_cantidad=0).exclude(diferencia_cantidad__isnull=True)
    for det_conteo in qs:
        ajuste = Ajuste(
            detalle_productos=det_conteo,
            productosenbodega = det_conteo.productosenbodega,
            bodega = det_conteo.bodega,
            producto = det_conteo.producto,
            nivel = det_conteo.nivel,
            seccion = det_conteo.seccion,
            diferencia_cantidad = det_conteo.diferencia_cantidad,
            tipo_diferencia = det_conteo.tipo_diferencia,
            #estado='Por aprobar'
        )
        ajuste.save()
    mensaje = "ok"
    return JsonResponse({"mensaje": mensaje})

