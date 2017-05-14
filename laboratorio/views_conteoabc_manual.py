# coding=utf-8

import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from laboratorio import views_busqueda_producto
from django.db.models import Q
from django.db import connection
from datetime import datetime, timedelta
from laboratorio.modelos_vista import Convertidor, json_default, ConteoABCVista
from laboratorio.models import Tipo, Producto, Bodega, ConteoInventario


@csrf_exempt
def ir_conteosabc(request):
    return render(request, "laboratorio/ver_conteos_abc.html")

"""Metodo obtener conteos abc.
HU: EC-LCINV-20: Adicionar conteo abc manual
Sirve para obtener los conteos de inventario abc que tiene el sistema
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtener_conteos_abc(request):
    qs = ConteoInventario.objects.all()
    listaConteos = []
    for conteo in qs:
        c = ConteoABCVista()
        c.id = conteo.id
        if conteo.usuario_creacion != None:
            c.nombreUsuarioCreacion = conteo.usuario_creacion.first_name + " " + conteo.usuario_creacion.last_name
        else:
            c.nombreUsuarioCreacion = " "
        c.estado = conteo.estado.nombre
        dh = timedelta(hours=5)
        c.fechaCreacion = (conteo.fecha_creacion - dh).strftime("%c")
        listaConteos.append(c)
    json_string = json.dumps(listaConteos, cls=Convertidor)
    return JsonResponse(json_string, safe=False)