# coding=utf-8

import decimal
import json
import time
from datetime import datetime
from django.utils.timezone import localtime
from operator import attrgetter

from decimal import Decimal

import sys
from django.core import serializers

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse, HttpResponse

from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from psycopg2.extensions import JSON

from laboratorio.modelos_vista import BodegaVista, Convertidor, ProductoVista, ProductosBodegaVista, RecursoBusquedaVista, RecursoBusquedaDetalleVista, TransaccionVista, json_default
from laboratorio.models import Tipo, Usuario, Bodega, Experimento, ProductoProtocolo, Producto, Protocolo
from laboratorio.models import TransaccionInventario, Producto, ProductosEnBodega
from laboratorio.utils.utils import utils

"""Metodo a navegar pie de pagina.
"""
def ir_ver_ordenes_producto(request):
    return render(request, "laboratorio/ver_ordenes_pedido.html")

