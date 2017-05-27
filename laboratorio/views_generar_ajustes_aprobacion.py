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
from laboratorio.models import Tipo, Usuario, Bodega, TransaccionInventario, ProductosEnBodega, Producto, ConteoInventario
from django.shortcuts import render


'''
Recibe el numero de conteo de inventario
Selecciona todos los registros de dicho conteo que tengan una diferencia entre lo contado automatica y fisicamente
Por cada uno de los registros se inserta un regristo en la tabla de ajustes
'''

@csrf_exempt
def generarAjustesConteo(request):


    if request.method == 'POST':
        conteoInvId = request.POST['id_conteo']
        cerrada_conAjuste = False
        print >> sys.stdout, "conteo:" + str(conteoInvId)
        cnt = ConteoInventario.objects.get(pk=conteoInvId)
        qs = DetalleProductos.objects.filter(conteoinventario=conteoInvId).exclude(diferencia_cantidad=0).exclude(diferencia_cantidad__isnull=True).exclude(estado__isnull=False)
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
                estado=Tipo.objects.get(pk=Tipo.objects.filter(nombre='En aprobacion', grupo='AJUSTE').first().id),

            )
            det_conteo.estado = Tipo.objects.get(pk=Tipo.objects.filter(nombre='Ajustes', grupo='STATUSCONTEO').first().id)
            det_conteo.save()
            cerrada_conAjuste = True
            ajuste.save()
        if cerrada_conAjuste:
            mensaje = "con ajustes por aprobar"
            cnt.estado=Tipo.objects.get(pk=Tipo.objects.filter(nombre='Cerrado con ajuste', grupo='STATUSCONTEO').first().id)
        else:
            mensaje = "sin novedades"
            cnt.estado = Tipo.objects.get(
                pk=Tipo.objects.filter(nombre='Cerrada', grupo='STATUSCONTEO').first().id)
        cnt.save()

        return JsonResponse({"mensaje": mensaje})

