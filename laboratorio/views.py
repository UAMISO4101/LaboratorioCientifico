# coding=utf-8

import json
import time
import sys

from datetime import datetime
from decimal import Decimal

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from laboratorio.modelos_vista import Convertidor, ProductoVista, ProductosBodegaVista
from laboratorio.models import Tipo, Usuario, Bodega, Experimento, ProductoProtocolo, Protocolo
from laboratorio.models import Producto, ProductosEnBodega
from laboratorio.utils.utils import utils
from laboratorio import views_nivel_insumos

# Navegacion de paginas

"""Metodo a navegar index.
"""
def ir_index(request):
    return render(request,"laboratorio/index.html")

"""Metodo a navegar pie de pagina.
"""
def ir_pie(request):
    return render(request,"laboratorio/pie.html")

"""Metodo a navegar encabezado.
"""
def ir_encabezado(request):
    return render(request,"laboratorio/encabezado.html")

"""Metodo obtener los tipos de unidad de medida.
HU: EC-LCINV4 - EC-LCINV14: Mostrar Unidades de Medida
Sirve para obtener de la tabla Tipos los tipos de unidad de medida
request, es la peticion dada por el usuario
return, formato json con los tipos de unidad de medida
"""
@csrf_exempt
def obtenerUnidadesMedida(request):
    qs = Tipo.objects.filter(grupo__contains="CONVERSION").distinct('nombre')
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)

"""Metodo obtenerTipo.
HU: EC-LCINV4: Insumes Volumen, Peso
Sirve para la consulta de un tipo en especifico
request, es la peticion dada por el usuario
return, formato json del tipo
"""
@csrf_exempt
def obtenerTipo(request):
    qs = Tipo.objects.filter(id=request.GET['id_tipo'])
    qs_json = serializers.serialize('json', qs)
    struct = json.loads(qs_json)
    json_tipo = json.dumps(struct[0])
    return JsonResponse({"tipo": json_tipo})

# HU-LCINV-13
# GZ
#Funcion GET que trae listas de valores segun el tipo
@csrf_exempt
def obtenerTipos(request):
    grupo = request.GET['grupo']
    qs = Tipo.objects.filter(grupo=grupo)
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)

# HU-LCINV-13
# GZ
# Obtiene los productos de la bodega seleccionada
@csrf_exempt
def obtenerProductosBodega(request):
    bodega = request.GET['bodega']
    pb_bodAll = ProductosEnBodega.objects.filter(bodega=Bodega.objects.get(pk=bodega))
    pb_bod = pb_bodAll.filter(cantidad__gt=0)
    listaProductosBodegas = []

    for productoBodega in pb_bod:
        pb = ProductosBodegaVista()
        pb.id = productoBodega.id
        pb.bodega = productoBodega.bodega.pk
        pb.producto = Producto.objects.get(pk=productoBodega.producto.pk).nombre
        pb.prod_id = Producto.objects.get(pk=productoBodega.producto.pk).pk
        pb.cantidad = productoBodega.cantidad
        pb.nivel = productoBodega.nivel
        pb.seccion = productoBodega.seccion
        pb.unidad_medida = Tipo.objects.get(pk=productoBodega.unidad_medida.id).nombre
        listaProductosBodegas.append(pb)
    json_pb = json.dumps(listaProductosBodegas, cls=Convertidor)
    return JsonResponse(json_pb, safe=False)        
        
# HU-LCINV-12
# DA
# Obtiene los experimentos en la aplicacion
@csrf_exempt
def obtenerExperimentos(request):
    qs = Experimento.objects.all().prefetch_related('asignado')
    qs_json = serializers.serialize('json', qs)
    respT = []
    for exp in qs:
        asignado = exp.asignado.values('username', 'id')[0]
        struct = json.loads(qs_json)[0]
        resp = {'experimento': struct, 'asignado': asignado}
        respT.append(resp)
    return JsonResponse(respT, safe=False)

# HU-LCINV-12
# DA
# Obtiene los experimentos en la aplicacion por username del usuario 'username'
@csrf_exempt
def obtenerExperimentosPorUsuario(request):
    usuario = Usuario.objects.get(username=request.GET['username'])
    exp_usuario = Experimento.objects.filter(asignado=usuario)
    qs_json = serializers.serialize('json', exp_usuario)
    return JsonResponse(qs_json, safe=False)

# HU-LCINV-12
# DA
# Obtiene los protocolos asociados a un experimento segun su codigo 'codigo'
@csrf_exempt
def obtenerProtocolosPorExperimento(request):
    exp = Experimento.objects.filter(codigo=request.GET['codigo'])
    prots_exp = Protocolo.objects.filter(experimento=exp)
    qs_json = serializers.serialize('json', prots_exp)
    return JsonResponse(qs_json, safe=False)

# HU-LCINV-12
# DA
# Los productosprotocolo (objeto con enlace a un producto y la cantidad usada por el mismo) por protocolo segun su id
@csrf_exempt
def obtenerPPPorProtocolo(request):
    prot = Protocolo.objects.filter(id=request.GET['id'])
    prods_prot = ProductoProtocolo.objects.filter(protocolo=prot).select_related('producto')
    qs_json = serializers.serialize('json', prods_prot)
    producto = {'nombre':prods_prot.first().producto.nombre,
                'id': prods_prot.first().producto.pk}
    struct = json.loads(qs_json)[0]
    resp = {'productoprotocolo': struct, 'producto': producto}
    return JsonResponse(resp, safe=False)

# HU-LCINV-12
# DA
# Hace el render de la plantilla para la visualización de productos/insumos por experimento
def experimentos(request):
    return render(request, "laboratorio/experimentos.html")

#HU: SA-LCINV-3
#SA
#Metodo que representa el servicio REST para retornar un JSON con un arreglo las medidas (unidades del S.I)
#con las que se caracteriza un recurso
@csrf_exempt
def obtenerTiposMedida(request):
    qs = Tipo.objects.filter(grupo="MEDIDAPRODUCTO")
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)

#HU: LCINV-4, 12
#SA - EC
#Metodo que representa el servicio REST para la conversion de unidades que sera
#invocado en la capa de presentacion, retorna el valor numerico de la conversion solicitada en formato JSON
@csrf_exempt
def convertirUnidad(request):
    cantidad = request.GET['cantidad']
    medidaOrigen = request.GET['medidaOrigen']
    medidaDestino = request.GET['medidaDestino']
    res = utils.convertir(cantidad=cantidad, medidaOrigen=medidaOrigen, medidaDestino=medidaDestino)
    return JsonResponse({"conversion":res})
