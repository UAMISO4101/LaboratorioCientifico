# coding=utf-8

import json
import time
from django.core import serializers
from datetime import datetime, timedelta
from decimal import Decimal
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from laboratorio.modelos_vista import BodegaVista, Convertidor
from laboratorio.models import Tipo, Usuario, Bodega
from django.shortcuts import render

"""Metodo a navegar crear bodega.
"""
def ir_crear_bodega(request):
    return render(request, "laboratorio/crearBodega.html")

"""Metodo a navegar lista de bodegas.
"""
def ir_bodegas(request):
    return render(request, "laboratorio/bodegas.html")

"""Metodo crear bodega.
HU: EC-LCINV2: Crear Bodega
Sirve para la creacion o actualizacion de bodegas del sistema
request, es la peticion dada por el usuario
return, formato json con un mensaje indicando si fue exitoso o no
"""
@csrf_exempt
def crearBodega(request):
    mensaje = ""
    if request.method == 'POST':
        dosLugares = Decimal('00.01')
        if request.POST.get('id_bodega_guardada', None) == None or request.POST.get('id_bodega_guardada', None) == "":
            bodega = Bodega(serial=request.POST['serial'],
                        nombre=request.POST['nombre'],
                        niveles=int(request.POST['niveles']),
                        secciones=int(request.POST['secciones']),
                        temperatura_minima=Decimal(request.POST['temperatura_minima']),
                        temperatura_media=Decimal(request.POST['temperatura_media']),
                        ubicacion = request.POST['ubicacion'],
                        fecha_creacion = datetime.now(),
                        tipo_bodega = Tipo.objects.filter(id=request.POST['tipo_bodega']).first(),
                        usuario=Usuario.objects.filter(id=request.POST['responsable']).first(),
                        unidad_medida=Tipo.objects.filter(id=request.POST['unidad_medida']).first())

            if not Bodega.objects.filter(serial=bodega.serial).exists():
                bodega.temperatura_minima.quantize(dosLugares, 'ROUND_DOWN')
                bodega.temperatura_media.quantize(dosLugares, 'ROUND_DOWN')
                bodega.save()
                mensaje = "ok"
            else:
                mensaje = "La bodega con ese serial ya existe"
        else:
            bodegass = Bodega.objects.filter(id=int(request.POST['id_bodega_guardada']))
            if (bodegass.exists()):
                bodega = bodegass.first()
                bodega.serial=request.POST['serial']
                bodega.nombre=request.POST['nombre']
                bodega.niveles = int(request.POST['niveles'])
                bodega.secciones = int(request.POST['secciones'])
                bodega.temperatura_minima =Decimal(request.POST['temperatura_minima'])
                bodega.temperatura_media =Decimal(request.POST['temperatura_media'])
                bodega.ubicacion = request.POST['ubicacion']
                bodega.tipo_bodega = Tipo.objects.filter(id=request.POST['tipo_bodega']).first()
                bodega.usuario = Usuario.objects.filter(id=request.POST['responsable']).first()
                bodega.unidad_medida = Tipo.objects.filter(id=request.POST['unidad_medida']).first()

                bodegaBDs = Bodega.objects.filter(serial=bodega.serial)
                actualizar = True
                if bodegaBDs.exists() and bodega.id != bodegaBDs.first().id:
                    actualizar = False

                if actualizar:
                    bodega.temperatura_minima.quantize(dosLugares, 'ROUND_DOWN')
                    bodega.temperatura_media.quantize(dosLugares, 'ROUND_DOWN')
                    bodega.fecha_actualizacion = datetime.now()
                    bodega.save()
                    mensaje = "ok"
                else:
                    mensaje = "La bodega con ese serial ya existe"

    return JsonResponse({"mensaje": mensaje})

@csrf_exempt
def obtenerBodegas(request, tipo_bodega = None):
    if tipo_bodega == None:
        qs = Bodega.objects.all()
    else:
        qs = Bodega.objects.filter(tipo_bodega=Tipo.objects.get(nombre=tipo_bodega))
    listaBodegas = []
    for bodega in qs:
        bod = BodegaVista()
        bod.id = bodega.id
        bod.nombre = bodega.nombre
        bod.serial = bodega.serial
        bod.niveles = bodega.niveles
        bod.secciones = bodega.secciones
        bod.temperatura_minima = str(bodega.temperatura_minima)
        bod.temperatura_media = str(bodega.temperatura_media)
        bod.ubicacion = bodega.ubicacion
        bod.tipo_bodega = bodega.tipo_bodega.nombre
        bod.unidad_medida = bodega.unidad_medida.nombre
        if bodega.estado:
            bod.estado = "Activo"
        else:
            bod.estado = "Inactivo"
        bod.responsable = bodega.usuario.first_name + " " + bodega.usuario.last_name
        listaBodegas.append(bod)
    json_string = json.dumps(listaBodegas, cls=Convertidor)
    return JsonResponse(json_string, safe=False)

"""Metodo obtenerBodega.
HU: EC-LCINV2: Crear Bodega
Sirve para la consulta de una bodega en especifica
request, es la peticion dada por el usuario
return, formato json de la bodega
"""
@csrf_exempt
def obtenerBodega(request):
    time.sleep(0.3)
    qs = Bodega.objects.filter(id=request.GET['id_bodega'])
    qs_json = serializers.serialize('json', qs)
    struct = json.loads(qs_json)
    json_bodega = json.dumps(struct[0])
    return JsonResponse({"bodega": json_bodega})

"""Metodo obtener los tipos de bodega.
HU: EC-LCINV2: Crear Bodega
Sirve para obtener de la tabla Tipos los tipos de bodega en el sistema
request, es la peticion dada por el usuario
return, formato json con los tipos de bodega
"""
@csrf_exempt
def obtenerTiposBodega(request):
    qs = Tipo.objects.filter(grupo="BODEGA")
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)