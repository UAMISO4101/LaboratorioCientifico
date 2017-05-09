# coding=utf-8
import json
from decimal import Decimal

import sys
from django.core import serializers
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from laboratorio.models import Producto, Tipo, Usuario, OrdenPedido, Rol, Bodega, DetalleOrden


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
    mensaje = ""
    if request.method == "POST":
        pk_producto = request.POST.get('producto', None)
        print >> sys.stdout, str(pk_producto)
        pk_orden = request.session.get('orden_pedido_id', None)
        fecha_movimiento = request.POST.get('fecha_movimiento', None)
        cantidad = request.POST.get('cantidad', None)
        bodega_id = request.POST.get('bodega', None)
        nivel = request.POST.get('nivel', None)
        seccion = request.POST.get('seccion', None)
        if pk_producto != None and pk_orden != None and fecha_movimiento != None and cantidad != None and bodega_id != None and nivel != None and seccion != None:
            producto = Producto.objects.get(id=pk_producto)
            orden = OrdenPedido.objects.get(id=pk_orden)
            fecha = datetime.strptime(fecha_movimiento, '%c')
            cant = Decimal(cantidad)
            bodega = Bodega.objects.get(id=bodega_id)
            level = int(nivel)
            secc = int(seccion)
            detalle = DetalleOrden()
            detalle.bodega = bodega
            detalle.fecha_movimiento = fecha
            detalle.producto = producto
            detalle.cantidad = cant
            detalle.nivel_bodega_destino = level
            detalle.seccion_bodega_destino = secc
            detalle.estado = Tipo.objects.filter(grupo="DETALLEPEDIDO", nombre="Recibido").first()
            detalle.orden = orden
            detalle.save()
            mensaje = "ok"
            del request.session['orden_pedido_id']
            del request.session['producto_id']
        else:
            mensaje = "Todos los campos deben ser diligenciados."
    return JsonResponse({'mensaje':mensaje})

@csrf_exempt
def fechaPeticionOrdenReposicion(request):

    pk_orden = request.session.get('orden_pedido_id', None)
    if pk_orden != None:
        orden = OrdenPedido.objects.get(id=pk_orden)
        fechaPeticion = orden.fecha_peticion.strftime('%c')
        return JsonResponse({"fecha": fechaPeticion})