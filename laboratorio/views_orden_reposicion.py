# coding=utf-8
import json

from django.core import serializers
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from laboratorio.models import Producto, Tipo, Usuario, OrdenPedido, Rol

def ir_modal_or(request):
    return render(request, "laboratorio/modal_orden_reposicion.html")

@csrf_exempt
def crearOrdenPedido(request):

    pk_producto = request.session.get('producto_id', None)
    if pk_producto != None:
        producto = Producto.objects.get(id=pk_producto)
        proveedor = producto.proveedor
        fecha_actual = datetime.now()
        estado = Tipo.objects.get(nombre="Ingresada")
        usuario_creacion = Usuario.objects.filter(is_superuser=False).exclude(roles__nombre = 'Proveedor').first()
        observaciones = "Orden de Reposición por nivel mínimo generada automáticamente."
        orden_pedido = OrdenPedido(fecha_peticion=fecha_actual,
                                   estado=estado,
                                   usuario_creacion=usuario_creacion,
                                   proveedor=proveedor,
                                   observaciones=observaciones)
        orden_pedido.save()
        mensaje = "ok"
        request.session['orden_pedido_id'] = orden_pedido.id
    else:
        mensaje = "Error al crear la orden de reposición"
    return JsonResponse({'mensaje':mensaje})

@csrf_exempt
def obtenerInfoProducto(request):

    pk_producto = request.session.get('producto_id', None)
    pk_orden = request.session.get('orden_pedido_id', None)
    if pk_producto != None and pk_orden != None:
        producto = Producto.objects.get(id=pk_producto)
        prod_json = json.loads(serializers.serialize('json', [producto]))
        return JsonResponse({'producto':prod_json, 'pk_orden':pk_orden}, safe=False)

@csrf_exempt
def guardarDetalleOrdenReposicion(request):
    return None