# coding=utf-8
import json
from decimal import Decimal

import sys
from django.core import serializers
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from laboratorio import views_nivel_insumos
from laboratorio.modelos_vista import Convertidor, ProductoVista
from laboratorio.models import Producto, Tipo, Usuario, OrdenPedido, Bodega, DetalleOrden, ProductoReposicionPendiente


def ir_modal_or(request):
    return render(request, "laboratorio/modal_orden_reposicion.html")

@csrf_exempt
def crearOrdenPedido(request):
    if request.method == 'GET' and 'id' in request.GET:
        id = request.GET['id']
        orden_pedido = crearOrden(id=id)
        request.session['producto_id'] = id
        request.session['orden_pedido_id'] = orden_pedido.id
        mensaje = "ok"
    else:
        pk_producto = request.session.get('producto_id', None)
        print >> sys.stdout, 'ID PRODUCTO crear' + str(request.session.get('producto_id', None))
        orden_pedido = crearOrden(id=pk_producto)
        mensaje = "ok"
        request.session['orden_pedido_id'] = orden_pedido.id

    return JsonResponse({'mensaje':mensaje})

@csrf_exempt
def obtenerInfoProducto(request):

    pk_producto = request.session.get('producto_id', None)
    pk_orden = request.session.get('orden_pedido_id', None)
    print >> sys.stdout, 'ID PRODUCTO info' + str(request.session.get('producto_id', None)) + ' '+ str(request.session.get('orden_pedido_id', None))
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
        bodega_id = request.POST.get('bodegaaa', None)
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
            if ProductoReposicionPendiente.objects.filter(producto_id=pk_producto).exists() == True:
                prodRes = ProductoReposicionPendiente.objects.get(producto_id=pk_producto)
                prodRes.detalle_orden_guardada = True
                prodRes.save()
            mensaje = "ok"
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

@csrf_exempt
def guardarNotificacionOrden(request):

    if request.method == 'GET' and 'id' in request.GET:
        id = request.GET['id']
        json_res = guardarDetalle(id=id)
        return json_res
    else:
        pk_producto = request.session.get('producto_id', None)
        json_res = guardarDetalle(id=pk_producto)
        return json_res

@csrf_exempt
def obtenerProductosPendienteReposicion(request):

    productos = ProductoReposicionPendiente.objects.all()
    listaProductos = []
    for producto in productos:
        produc = Producto.objects.get(id=producto.producto_id)
        prod = ProductoVista()
        prod.id = produc.id
        prod.codigo = produc.codigo
        prod.nombre = produc.nombre
        prod.descripcion = produc.descripcion
        prod.valorUnitario = str(produc.valorUnitario)
        prod.unidadesExistentes = str(produc.unidadesExistentes)
        prod.clasificacion = produc.get_clasificacion_display()
        prod.unidad_medida = produc.unidad_medida.nombre
        prod.unidad_unitaria = str(produc.unidad_unitaria)
        prod.imageFile = str(produc.imageFile)
        prod.proveedor = produc.proveedor.first_name
        codigo_color = views_nivel_insumos.nivel_insumo_tabla(produc.id, produc.punto_pedido)
        prod.codigo_color = str(producto.detalle_orden_guardada)
        prod.punto_pedido = str(produc.punto_pedido)
        prod.nivel_actual = str(codigo_color[1])
        listaProductos.append(prod)
    json_string = json.dumps(listaProductos, cls=Convertidor)
    return JsonResponse({'productos':json_string})

def guardarDetalle(id):

    if id != None and ProductoReposicionPendiente.objects.filter(producto_id=id).exists() == False:
        producto = Producto.objects.get(id=id)
        productoReposicion = ProductoReposicionPendiente()
        productoReposicion.producto = producto
        productoReposicion.detalle_orden_guardada = False
        productoReposicion.save()
        return JsonResponse({'mensaje': 'ok'})
    else:
        return JsonResponse({'mensaje': 'YaExisteOrden'})

def crearOrden(id):

    if id != None:
        producto = Producto.objects.get(id=id)
        proveedor = producto.proveedor
        fecha_actual = datetime.now()
        estado = Tipo.objects.get(nombre="Ingresada")
        usuario_creacion = Usuario.objects.filter(is_superuser=False).exclude(roles__nombre='Proveedor').first()
        observaciones = "Orden de Reposición por nivel mínimo generada automáticamente."
        orden_pedido = OrdenPedido(fecha_peticion=fecha_actual,
                                   estado=estado,
                                  usuario_creacion=usuario_creacion,
                                  proveedor=proveedor,
                                  observaciones=observaciones)
        orden_pedido.save()
        return orden_pedido
