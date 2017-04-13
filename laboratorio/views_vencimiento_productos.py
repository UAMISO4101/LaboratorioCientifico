# coding=utf-8

import json
from django.utils.timezone import localtime
from operator import attrgetter

from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime

from laboratorio.modelos_vista import Convertidor, RecursoBusquedaVista, RecursoBusquedaDetalleVista
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

    busqueda_producto(request)
    return render(request, "laboratorio/productovencido.html")

# HU: LCINV-9
# FB.
# TODO: Descripcion
# request: Petición desde el form de usuario.
# return: json con los datos encontrados
def busqueda_producto(request):
    dias_anticipacion = "0"

    # Se obtiene la variable de los días, de la tabla Tipo. Esto para el semáforo.
    qsdias = Tipo.objects.filter(grupo="VENCIDOSDIASANTICIPACION").first()

    # TODO: Validacion por si no viene nada.
    if qsdias.nombre:
        dias_anticipacion = dias_anticipacion = qsdias.nombre

    # Traer los productos con su fecha de vencimiento, filtrando por las bodegas que solo sean responsabilidad
    # del Jefe de bodega
    qs = ProductosEnBodega.objects.all()

    # Se asigna la fecha actual a una variable
    fecha_actual = datetime.today()

    # Por cada producto se compara la fecha de vencimiento con la fecha actual.
    # De esta comparación salen
    # - Los vencidos.
    # - Los que se vencen desde la fecha actual hasta el día que el usuario definió como VENCIDOSDIASANTICIPACION.
    # - Los que la fecha de vencimiento es mayor que VENCIDOSDIASANTICIPACION.



    # Filtra por la expresion; si no hay nada, muestra todos los productos
#    if bproducto == "" and bBodega == "":  # Sin filtro
#        qs = ProductosEnBodega.objects.all()
#    else:  # Filtro
#        if bproducto != "" and bBodega == "":  # Si solo se filtra por producto
#            qs = ProductosEnBodega.objects.filter(producto__codigo=bproducto)
#        elif bproducto == "" and bBodega != "":  # Si solo se filtra por bodega
##            qs = ProductosEnBodega.objects.filter(bodega__serial=bBodega)
 ##       else:  # Filtro por producto y bodega
 #           qs = ProductosEnBodega.objects.filter(producto__codigo=bproducto, bodega__serial=bBodega)

    lista_recurso = []

 #   for peb in qs:
#        req = RecursoBusquedaVista()
#        req.id = peb.id
#        req.nombre = peb.producto.nombre
#        req.unidadesExistentes = peb.cantidad
#        req.unidad_medida = peb.producto.unidad_medida.nombre
#        req.fechaTransaccion = obtener_bodega_actualxpebxtransaccion(peb, 2)
#        # Convertir a unidades de preferencia
#        req.cantidad_convertida = str(utils.convertir(req.unidadesExistentes, peb.unidad_medida.nombre,
#                                                      peb.bodega.unidad_medida.nombre))
#
 #       localizacion = ""
#        if str(peb.nivel) != "":
#            localizacion = ", Nivel " + str(peb.nivel)
#        if str(peb.seccion) != "":
#            localizacion = localizacion + ", Seccion " + str(peb.seccion)

#        req.bodegaActual = peb.bodega.nombre + localizacion
#        # Variable oculta para debug en html
#        req.hidden1 = "bFechaTransaccion:" + bFechaTransaccion + " req.fechaTransaccion:" + req.fechaTransaccion + " pebbodega:" + str(peb.bodega.unidad_medida)

#        if bFechaTransaccion == "":
#            lista_recurso.append(req)
#        else:
#            if bFechaTransaccion in req.fechaTransaccion:
#                lista_recurso.append(req)

#   lista_recurso.sort(key=attrgetter('fechaTransaccion'), reverse=True)

    json_string = json.dumps(lista_recurso, cls=Convertidor)
    return JsonResponse(json_string, safe=False)
