# coding=utf-8

import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import connection
from datetime import datetime, timedelta
from laboratorio.modelos_vista import Convertidor, ProductoVencimientoVista, json_default
from laboratorio.models import TransaccionInventario, Tipo, Producto, Bodega


# HU: LCINV-9
# FB.
# Carga inicial de la página de productos vencidos.
# request: Petición desde el form de usuario.
# return: Página html con la plantilla y los resultados de la búsqueda asociada.
@csrf_exempt
def ver_vencimiento_producto(request):
    return render(request, "laboratorio/productovencido.html")


# HU: LCINV-9
# FB.
# Consulta la información de productos vencidos y le agrega la parte del semáforo.
# request: Petición desde el form de usuario.
# return: json con los datos encontrados
@csrf_exempt
def lista_vencidos(request):
    # Se obtiene la variable de los días, de la tabla Tipo. Esto para el semáforo.
    qsdias = Tipo.objects.filter(grupo="VENCIDOSDIASANTICIPACION")[:1]

    if qsdias.exists():
        dias_anticipacion = dias_anticipacion = qsdias[0].nombre
    else:
        dias_anticipacion = "0"

    # Se asigna la fecha futura para la comparación
    fecha_futura = datetime.now().date() + timedelta(days=int(dias_anticipacion))

    # Traer los productos con su fecha de vencimiento, filtrando por las bodegas que solo sean responsabilidad
    # del Jefe de bodega

    # Se obtienen las transacciones que no queremos contabilizar
    qst1 = Tipo.objects.filter(Q(nombre="'Traslado a experimento'") | Q(nombre="'Mover por perdida o desperdicio'") | Q(nombre="'Devolucion a proveedor'"))

    # Se filtra en las transacciones que no se desea que aparezcan
    qstran1 = TransaccionInventario.objects.filter(Q(tipo__in=qst1))  # .values('producto_bodega_destino').distinct()

    # Los productos que queden es porque no se han pasado a desperdicio, experimento o a devolución
    # qsprod = ProductosEnBodega.objects.exclude(id__in=TransaccionInventario.objects.filter(tipo__in=qst1.values_list('id', flat=True)).values_list('producto_bodega_destino_id', flat=True))
    # qsprod = ProductosEnBodega.objects.filter(id__in=qstran1.values('producto_bodega_destino_id').filter(id=18))
    # qsprod = ProductosEnBodega.objects.filter(~Q(
    #   id__in=TransaccionInventario.objects.filter(tipo__in=qst1.values_list('id', flat=True)).values_list(
    #       'producto_bodega_destino_id', flat=True)))
    # Nota: Se dejan las consultas para revisar luego por qué no funcionaron.

    qsprod = t3()

    # Por cada producto se compara la fecha de vencimiento con la fecha actual.
    # De esta comparación salen
    # - Los vencidos.
    # - Los que se vencen desde la fecha actual hasta el día que el usuario definió como VENCIDOSDIASANTICIPACION.
    # - Los que la fecha de vencimiento es mayor que VENCIDOSDIASANTICIPACION.
    lista_recurso = []

    # orden esperado
    # 0id, 1nivel, 2seccion, 3cantidad, 4bodega_id, 5producto_id, 6unidad_medida_id, 7fecha_vencimiento

    for peb in qsprod:
        req = ProductoVencimientoVista()
        # req.id = peb.id
        # req.producto = peb.producto.nombre
        # req.nivel = peb.nivel
        # req.seccion = peb.seccion
        # req.fecha_vencimiento = peb.fecha_vencimiento
        # req.dias_anticipacion = dias_anticipacion

        req.id = peb[0]
        req.producto = str(Producto.objects.filter(id=peb[5])[:1].values('nombre')[0]['nombre'])
        req.nivel = peb[1]
        req.seccion = peb[2]
        req.fecha_vencimiento = peb[7]
        req.dias_anticipacion = dias_anticipacion

        localizacion = ""

        if str(req.nivel) != "":
            localizacion = localizacion + ", Nivel " + str(req.nivel)
        if str(req.seccion) != "":
            localizacion = localizacion + ", Seccion " + str(req.seccion)

        # req.bodega = peb.bodega.nombre + localizacion
        req.bodega = str(Bodega.objects.filter(id=peb[4])[:1].values('nombre')[0]['nombre']) + localizacion

        # 1: Rojo: Ya vencidos, incluyen los que vencen hoy.
        # 2: Amarillo: Vencen mañana o dentro de "dias_anticipacion" días.
        # 3: Verde: Vencen después de de "dias_anticipacion" días.
        # 4: N/A: Sin fecha de vencimiento.

        if not req.fecha_vencimiento:
            semaforo = 4
            estado = "4. N/A"
        else:
            if req.fecha_vencimiento <= datetime.now().date():
                semaforo = 1
                estado = "1. Vencido"
            elif (req.fecha_vencimiento > datetime.now().date()) and (req.fecha_vencimiento <= fecha_futura):
                semaforo = 2
                estado = "2. Próximo a Vencer"
            else:
                semaforo = 3
                estado = "3. OK"

        req.semaforo_vencimiento = semaforo
        req.semaforo_estado = estado

        lista_recurso.append(req)

    json_string = json.dumps(lista_recurso, cls=Convertidor, default=json_default)
    return JsonResponse(json_string, safe=False)


# HU: LCINV-9
# FB.
# Consulta directa a la BD
# return: Listado filtrado con los productos que les aplica el vencimiento.
def t3():
    q = "SELECT * FROM ""laboratorio_productosenbodega"" WHERE NOT ""laboratorio_productosenbodega"".""id"" IN (SELECT V0.""producto_bodega_destino_id"" FROM ""laboratorio_transaccioninventario"" V0 WHERE V0.""tipo_id"" IN (SELECT U0.""id"" FROM ""laboratorio_tipo"" U0 WHERE (U0.""nombre"" = 'Traslado a experimento' OR U0.""nombre"" = 'Mover por perdida o desperdicio' OR U0.""nombre"" = 'Devolucion a proveedor')))"
    with connection.cursor() as c:
        c.execute(q)
        return list(c)
