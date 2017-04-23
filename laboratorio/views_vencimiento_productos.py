# coding=utf-8

import json
from django.utils.timezone import localtime
from operator import attrgetter

from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

from laboratorio.modelos_vista import Convertidor, ProductoVencimientoVista, json_default
from laboratorio.models import Usuario, Bodega, Tipo
from laboratorio.models import TransaccionInventario, Producto, ProductosEnBodega
from laboratorio.utils.utils import utils


# HU: LCINV-9
# FB.
# TODO: Descripcion
# request: Petición desde el form de usuario.
# return: Página html con la plantilla y los resultados de la búsqueda asociada.
@csrf_exempt
def ver_vencimiento_producto(request):
    # global bproducto
    # global bBodega
    # global bFechaTransaccion

    # bproducto = ""
    # bBodega = ""
    # bFechaTransaccion = ""

    # Capturar el valor de los campos
    if request.method == 'POST':
        bproducto = request.POST.get('producto', "")
        bBodega = request.POST.get('bodega', "")
        bFechaTransaccion = request.POST.get('fechatransaccion', "")

    lista_vencidos(request)
    return render(request, "laboratorio/productovencido.html")


# HU: LCINV-9
# FB.
# TODO: Descripcion
# request: Petición desde el form de usuario.
# return: json con los datos encontrados
@csrf_exempt
def lista_vencidos(request):
    dias_anticipacion = "0"

    # Se obtiene la variable de los días, de la tabla Tipo. Esto para el semáforo.
    qsdias = Tipo.objects.filter(grupo="VENCIDOSDIASANTICIPACION")[:1]

    if qsdias.exists():
        dias_anticipacion = dias_anticipacion = qsdias[0].nombre

    # Se asigna la fecha futura para la comparación
    fecha_futura = datetime.now().date() + timedelta(days=int(dias_anticipacion))

    # Traer los productos con su fecha de vencimiento, filtrando por las bodegas que solo sean responsabilidad
    # del Jefe de bodega
    # Traer todos los productos que no estén asignado a un proyecto o que se hayan desperdiciado
    # TODO: Afinar el filtro
    qsprod = ProductosEnBodega.objects.exclude(ubucacionDestino__tipo__nombre="'Traslado a experimento'")
    qsprod = qsprod.exclude(ubucacionDestino__tipo__nombre="'Mover por perdida o desperdicio'")

    # Por cada producto se compara la fecha de vencimiento con la fecha actual.
    # De esta comparación salen
    # - Los vencidos.
    # - Los que se vencen desde la fecha actual hasta el día que el usuario definió como VENCIDOSDIASANTICIPACION.
    # - Los que la fecha de vencimiento es mayor que VENCIDOSDIASANTICIPACION.
    lista_recurso = []

    for peb in qsprod:
        req = ProductoVencimientoVista()
        req.id = peb.id
        req.bodega = peb.bodega.nombre
        req.producto = peb.producto.nombre
        req.nivel = peb.nivel
        req.seccion = peb.seccion
        req.fecha_vencimiento = peb.fecha_vencimiento
        req.dias_anticipacion = dias_anticipacion

        # 1: Rojo: Ya vencidos, incluyen los que vencen hoy.
        # 2: Amarillo: Vencen mañana o dentro de "dias_anticipacion" días.
        # 3: Verde: Vencen después de de "dias_anticipacion" días.
        semaforo = "N/A"

        if not peb.fecha_vencimiento:
            semaforo = "N/D"
        else:
            if peb.fecha_vencimiento <= datetime.now().date():  # TODO: Sacar a los que se vencieron y ya los desecharon
                semaforo = "1"
            elif (peb.fecha_vencimiento > datetime.now().date()) and (peb.fecha_vencimiento <= fecha_futura):
                semaforo = "2"
            else:
                semaforo = "3"

        req.semaforo_vencimiento = semaforo
        lista_recurso.append(req)

    json_string = json.dumps(lista_recurso, cls=Convertidor, default=json_default)
    return JsonResponse(json_string, safe=False)