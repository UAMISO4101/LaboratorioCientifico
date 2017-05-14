# coding=utf-8

import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from laboratorio import views_busqueda_producto
from django.db.models import Q
from django.db import connection
from datetime import datetime, timedelta
from laboratorio.modelos_vista import Convertidor, ProductoVencimientoVista, json_default
from laboratorio.models import TransaccionInventario, Tipo, Producto, Bodega


# @csrf_exempt
#def ver_conteoabc(request):
#    return render(request, "laboratorio/conteoabc_manual.html")