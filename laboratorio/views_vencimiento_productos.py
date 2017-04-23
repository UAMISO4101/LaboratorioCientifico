# coding=utf-8

import json
from django.utils.timezone import localtime
from operator import attrgetter

from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from datetime import datetime, timedelta

from laboratorio.modelos_vista import Convertidor, ProductoVencimientoVista, json_default
from laboratorio.models import TransaccionInventario, Producto, ProductosEnBodega, Tipo
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

    # Se obtienen las transacciones que no queremos contabilizar
    qst1 = Tipo.objects.filter(Q(nombre="'Traslado a experimento'") | Q(nombre="'Mover por perdida o desperdicio'") | Q(nombre="'Devolucion a proveedor'"))

    # Se filtra en las transacciones

    qstran1 = TransaccionInventario.objects.filter(Q(tipo__in=qst1))  # .values('producto_bodega_destino').distinct()

    # Los productos que queden es porque no se han pasado a desperdicio, experimento o a devolución
    # qsprod = ProductosEnBodega.objects.exclude(id__in=qstran1.values('producto_bodega_destino_id'))

    qsprod = ProductosEnBodega.objects.exclude(id__in=
                        TransaccionInventario.objects.filter(tipo__in=
                        qst1.values_list('id', flat=True)).values_list('producto_bodega_destino_id', flat=True))

    # qsprod = ProductosEnBodega.objects.filter(id=8)
    # qsprod = ProductosEnBodega.objects.exclude(Q(id__in=qstran1['producto_bodega_destino_id']))
    # .order_by('fecha_vencimiento', '-producto', 'bodega', 'nivel', 'seccion')

    # Por cada producto se compara la fecha de vencimiento con la fecha actual.
    # De esta comparación salen
    # - Los vencidos.
    # - Los que se vencen desde la fecha actual hasta el día que el usuario definió como VENCIDOSDIASANTICIPACION.
    # - Los que la fecha de vencimiento es mayor que VENCIDOSDIASANTICIPACION.
    lista_recurso = []

    for peb in qsprod:
        req = ProductoVencimientoVista()
        req.id = peb.id
        req.producto = peb.producto.nombre
        req.nivel = peb.nivel
        req.seccion = peb.seccion
        req.fecha_vencimiento = peb.fecha_vencimiento
        req.dias_anticipacion = dias_anticipacion

        localizacion = ""

        if str(req.nivel) != "":
            localizacion = localizacion + ", Nivel " + str(req.nivel)
        if str(req.seccion) != "":
            localizacion = localizacion + ", Seccion " + str(req.seccion)

        req.bodega = peb.bodega.nombre + localizacion

        # 1: Rojo: Ya vencidos, incluyen los que vencen hoy.
        # 2: Amarillo: Vencen mañana o dentro de "dias_anticipacion" días.
        # 3: Verde: Vencen después de de "dias_anticipacion" días.
        # 4: N/A: Sin fecha de vencimiento.

        if not peb.fecha_vencimiento:
            semaforo = 4
            estado = "4. N/A"
        else:
            if peb.fecha_vencimiento <= datetime.now().date():
                semaforo = 1
                estado = "1. Vencido"
            elif (peb.fecha_vencimiento > datetime.now().date()) and (peb.fecha_vencimiento <= fecha_futura):
                semaforo = 2
                estado = "2. Próximo a Vencer"
            else:
                semaforo = 3
                estado = "3. OK"

        req.semaforo_vencimiento = semaforo
        req.semaforo_estado = estado

        lista_recurso.append(req)

        # lista_recurso = sorted(lista_recurso, key=attrgetter('semaforo_vencimiento', 'fecha_vencimiento'))

    json_string = json.dumps(lista_recurso, cls=Convertidor, default=json_default)
    return JsonResponse(json_string, safe=False)
