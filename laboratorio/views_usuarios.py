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

"""Metodo obtener los usuarios del sistema.
HU: EC-LCINV2: Crear Bodega
Sirve para obtener los usuarios que existen en el sistema
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtenerUsuarios(request):
    qs = Usuario.objects.all()
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)

#HU: SA-LCVIN-3
#SA
#Metodo que representa el servicio REST para obtener los proveedores actuales de insumos
#se retornara una lista de los proveedores en formato JSON
@csrf_exempt
def obtenerProveedores(request):

    proveedores = Usuario.objects.filter(roles__nombre="Proveedor")
    qs_json = serializers.serialize('json', proveedores)
    return JsonResponse(qs_json, safe=False)