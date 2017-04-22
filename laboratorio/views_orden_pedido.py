# coding=utf-8

import decimal
import json
import time

from datetime import datetime, timedelta

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

from laboratorio.modelos_vista import BodegaVista, Convertidor, ProductoVista, ProductosBodegaVista, RecursoBusquedaVista, RecursoBusquedaDetalleVista, TransaccionVista, json_default, \
    OrdenPedidoVista, DetalleOrdenVista
from laboratorio.models import Tipo, Usuario, Bodega, Experimento, ProductoProtocolo, Producto, Protocolo, OrdenPedido, \
    DetalleOrden, ComentarioOrden
from laboratorio.models import TransaccionInventario, Producto, ProductosEnBodega
from laboratorio.utils.utils import utils
from .views import ejecutar_transaccion

"""Metodo para navegar proceso de aprobacion.
"""
def proceso_aprobacion_orden(request):
    return render(request, "laboratorio/proceso_aprobacion_orden.html")

"""Metodo a navegar ordenes de pedido.
"""
def ir_ver_ordenes_pedido(request):
    return render(request, "laboratorio/ver_ordenes_pedido.html")

"""Metodo a navegar orden de pedido.
"""
def ir_orden_pedido(request):
    return render(request, "laboratorio/orden_pedido.html")

"""Metodo a navegar pie de pagina.
"""
def ir_modal_do(request):
    return render(request,"laboratorio/modal_detalle_orden.html")

"""Metodo obtener los usuarios del sistema sin proveedores y sin admin.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para obtener los usuarios que existen en el sistema que no son proveedores y no admin
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtenerSoloUsuarios(request):
    qs = Usuario.objects.filter(is_superuser=False).exclude(roles__nombre = 'Proveedor')
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)


"""Metodo obtener los estados de la orden de pedido.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para obtener los estados que puede tener una orden de pedido
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtenerEstadosOP(request):
    qs = Tipo.objects.filter(grupo='ORDENPEDIDO')
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)

"""Metodo obtener fecha actual.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para obtener la fecha actual del sistema
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtener_fecha_actual(request):
    fecha_actual = time.strftime("%c")
    return JsonResponse({"fecha": fecha_actual})

"""Metodo a navegar actualizar orden de pedido.
HU: EC-LCINV-17: Crear Orden de Pedido
"""
def ir_act_orden_pedido(request):
    return render(request, "laboratorio/act_orden_pedido.html")

"""Metodo a navegar para la recepcion de orden de pedido hechas previamente al proveedor.
HU: EC-LCINV-19: Recibir Orden de Pedido del proveedor
"""
def ir_recibir_orden_pedido(request):
    return render(request, "laboratorio/recibir_orden_pedido.html")


"""Metodo crear orden de pedido.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para crear una orden de pedido en el sistema
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def crear_orden_pedido(request):
    mensaje = ""
    if request.method == 'POST':
        orden_pedido = OrdenPedido(fecha_peticion=datetime.strptime(request.POST['fecha_creacion'], '%c'),
                        estado=Tipo.objects.filter(id=request.POST['estado']).first(),
                        usuario_creacion=Usuario.objects.filter(id=request.POST['usuario_creacion']).first(),
                        proveedor=Usuario.objects.filter(id=request.POST['proveedor']).first(),
                        observaciones=request.POST['observaciones'])

        orden_pedido.save()
        mensaje = orden_pedido.id

    return JsonResponse({"id": mensaje})

"""Metodo obtener orden de pedido.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para obtener la orden de pedido dado el id de la orden
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtener_op(request):
    time.sleep(0.3)
    qs = OrdenPedido.objects.filter(id=request.GET['id_op'])
    qs_json = serializers.serialize('json', qs)
    struct = json.loads(qs_json)
    json_op = json.dumps(struct[0])
    return JsonResponse({"op": json_op})

"""Metodo obtener orden de pedido.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para obtener la orden de pedido dado el id de la orden
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtener_fecha_peticion_op(request):
    qs = OrdenPedido.objects.filter(id=request.GET['id_op'])
    orden_pedido = qs.first()
    dh = timedelta(hours=5)
    return JsonResponse({"fecha_peticion": (orden_pedido.fecha_peticion - dh).strftime("%c")})


"""Metodo obtener ordenes de pedido.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para obtener las ordenes de pedido que tiene el sistema
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtenerOrdenesPedido(request):
    qs = OrdenPedido.objects.all()
    listaOps = []
    for orden_pedido in qs:
        orden = OrdenPedidoVista()
        orden.id = orden_pedido.id
        if orden_pedido.usuario_creacion != None:
            orden.nombreUsuarioCreacion = orden_pedido.usuario_creacion.first_name + " " + orden_pedido.usuario_creacion.last_name
        else:
            orden.nombreUsuarioCreacion = " "
        if orden_pedido.usuario_aprobacion != None:
            orden.nombreUsuarioAprobacion = orden_pedido.usuario_aprobacion.first_name + " " + orden_pedido.usuario_aprobacion.last_name
        else:
            orden.nombreUsuarioAprobacion = " "
        if orden_pedido.proveedor != None:
            orden.nombreProveedor = orden_pedido.proveedor.first_name + " " + orden_pedido.proveedor.last_name
        else:
            orden.nombreProveedor = " "
        orden.estado = orden_pedido.estado.nombre
        dh = timedelta(hours=5)
        orden.fechaPeticion = (orden_pedido.fecha_peticion - dh).strftime("%c")
        listaOps.append(orden)
    json_string = json.dumps(listaOps, cls=Convertidor)
    return JsonResponse(json_string, safe=False)

"""Metodo obtener los usuarios del sistema sin proveedores y sin admin.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para obtener los usuarios que existen en el sistema que no son proveedores y no admin
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtenerProductos(request):
    prov=Usuario()
    prov.id = request.GET["id_proveedor"];
    qs = Producto.objects.filter(proveedor=prov)
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)

"""Metodo guardar orden de pedido y detalle de la orden.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para atualizar una orden de pedido en el sistema y
para guardar el detalle de la orden
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def guardarOrdenDetalle(request):
    mensaje = ""
    if request.method == 'POST':
        orden_cliente = json.loads(request.body)
        ordenes_pedido = OrdenPedido.objects.filter(id=orden_cliente['id'])
        if ordenes_pedido.exists():
            orden_pedido = ordenes_pedido.first()
            orden_pedido.observaciones = orden_cliente['observaciones']
            orden_pedido.usuario_creacion=Usuario.objects.filter(id=orden_cliente['idUsuarioCreacion']).first()
            orden_pedido.proveedor=Usuario.objects.filter(id=orden_cliente['idProveedor']).first()
            orden_pedido.estado=Tipo.objects.filter(id=orden_cliente['idEstado']).first()
            orden_pedido.save()

            detallesOrden = DetalleOrden.objects.filter(orden=orden_pedido)
            if detallesOrden.exists():
                for det in detallesOrden:
                    det.delete()

            for item in orden_cliente["items"]:
                detalle = DetalleOrden()
                detalle.fecha_movimiento = datetime.strptime(item["fechaMovimiento"], '%c')
                detalle.cantidad = item["cantidad"]
                detalle.producto = Producto.objects.filter(id=item["idProducto"]).first()
                detalle.bodega = Bodega.objects.filter(id=item["idBodega"]).first()
                detalle.estado = Tipo.objects.filter(grupo="DETALLEPEDIDO",nombre="Recibido").first()
                detalle.nivel_bodega_destino = item["nivel"]
                detalle.seccion_bodega_destino = item["seccion"]
                detalle.orden = orden_pedido
                detalle.save()

        mensaje = "ok"
    return JsonResponse({"mensaje": mensaje})

"""Metodo obtener detalle ordenes de una orden.
HU: EC-LCINV-17: Crear Orden de Pedido
Sirve para obtener detalle ordenes de una orden
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtener_do(request):
    qs = DetalleOrden.objects.filter(orden=request.GET['id_op'])
    listaDO = []
    if qs.exists():
        for det_orden in qs:
            detalleOrden = DetalleOrdenVista()
            detalleOrden.idProducto = det_orden.producto.id
            detalleOrden.nombreProducto = det_orden.producto.nombre
            detalleOrden.valorUnitario = int(det_orden.producto.valorUnitario)
            detalleOrden.idBodega = det_orden.bodega.id
            detalleOrden.nombreBodega = det_orden.bodega.nombre
            detalleOrden.cantidad = int(det_orden.cantidad)
            detalleOrden.nivel = det_orden.nivel_bodega_destino
            detalleOrden.seccion = det_orden.seccion_bodega_destino
            detalleOrden.estado=Tipo.objects.get(pk=det_orden.estado.pk).nombre
            detalleOrden.transaccion_inventario=det_orden.transaccion_inventario_id
            dh = timedelta(hours=5)
            detalleOrden.fechaMovimiento = (det_orden.fecha_movimiento - dh).strftime("%c")
            listaDO.append(detalleOrden)

    json_string = json.dumps(listaDO, cls=Convertidor)
    return JsonResponse(json_string, safe=False)



#HU-LCINV-19
#GZ
#Crea transacciones de inventario por cada item en un pedido recibido del proveedor:
#La bodega origen siempre es proveedor
#Bodega destino con localizacion (Nivel, Seccion)
#Producto y cantidad a mover

@csrf_exempt
def ejecutar_transacciones_orden(request):
    mensaje = ""
    if request.method == 'POST':
        orden_cliente = json.loads(request.body)
        qs_val = DetalleOrden.objects.filter(orden=orden_cliente['id'], bodega__bodegaDestino=None)

        qs = DetalleOrden.objects.filter(orden=orden_cliente['id'], transaccion_inventario_id=None)
        for det_orden in qs:
            transaccion = TransaccionInventario(
                tipo=Tipo.objects.get(nombre='Recepcion de Proveedor', grupo='TIPOTRX'),
                bodega_origen=Bodega.objects.get(nombre='Proveedor'),
                nivel_origen=1,
                seccion_origen=1,
                bodega_destino=Bodega.objects.get(pk=det_orden.bodega_id),
                nivel_destino=det_orden.nivel_bodega_destino,
                seccion_destino=det_orden.seccion_bodega_destino,
                producto=det_orden.producto,
                cantidad=det_orden.cantidad,
                unidad_medida=Tipo.objects.get(pk=det_orden.producto.unidad_medida_id),
                estado=Tipo.objects.get(pk=Tipo.objects.filter(nombre='Ejecutada', grupo='STATUSTRX').first().id),
                fecha_creacion=datetime.now(),
                fecha_ejecucion=datetime.now(),
                usuario=Usuario.objects.get(pk=1),
                comentarios='Transacción Automática Orden No' + str(orden_cliente['id'])
            )
            transaccion.save()
            ejecutar_transaccion(transaccion)

            det_orden.estado_id = Tipo.objects.get(pk=Tipo.objects.filter(nombre='Movida', grupo='DETALLEPEDIDO').first().id)
            det_orden.transaccion_inventario_id = transaccion.pk
            det_orden.save()
        orden = OrdenPedido.objects.get(pk=orden_cliente['id'])
        orden.estado_id = Tipo.objects.get(pk=Tipo.objects.filter(nombre='Recibida', grupo='ORDENPEDIDO').first().id)
        orden.save()
    mensaje = "ok"
    return JsonResponse({"mensaje": mensaje})

"""Metodo obtener aprobar una orden.
HU: DA-LCINV-18: Cientifico lider aprueba orden de pedido
Sirve para aprobar una orden dada por su id
request, es la peticion dada por el usuario
return, formato json con mensaje de confirmación
"""
@csrf_exempt
def aprobar_orden(request):
    aprobacion = json.loads(request.body)
    orden = OrdenPedido.objects.get(id=aprobacion['id_op'])
    comentario = ComentarioOrden(timestamp=datetime.now(), comentario=aprobacion['comentario'], orden=orden)
    comentario.save()
    orden.estado = Tipo.objects.get(nombre='Aprobada')
    orden.save()
    return JsonResponse({"mensaje": 'ok'})

"""Metodo rechazar una orden.
HU: DA-LCINV-18: Cientifico lider aprueba orden de pedido
Sirve para rechazar una orden dada por su id
request, es la peticion dada por el usuario
return, formato json con mensaje de confirmación
"""
@csrf_exempt
def rechazar_orden(request):
    rechazo = json.loads(request.body)
    orden = OrdenPedido.objects.get(id=rechazo['id_op'])
    comentario = ComentarioOrden(timestamp=datetime.now(), comentario=rechazo['comentario'], orden=orden)
    comentario.save()
    orden.estado = Tipo.objects.get(nombre='Rechazada')
    orden.save()
    return JsonResponse({"mensaje": 'ok'})

"""Metodo obtener comentarios de una orden.
HU: DA-LCINV-18: Cientifico lider aprueba orden de pedido
Sirve para obtener comentarios de una orden
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtener_comentarios_orden(request):
    time.sleep(0.3)
    qs = ComentarioOrden.objects.filter(orden=request.GET['id_op'])
    qs_json = serializers.serialize('json', qs)
    struct = json.loads(qs_json)
    if len(struct) > 0:
        json_op = json.dumps(struct[0])
    else:
        json_op = []
    return JsonResponse(qs_json, safe=False)

"""Metodo para cambiar de estado orden aprobada a en proveedor.
HU: DA-LCINV-18: Cientifico lider aprueba orden de pedido
Sirve para obtener cambiar estado de 'Aprobada' a 'En proveedor'
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def cambiar_aprobada_en_proveedor(request):
    orden = OrdenPedido.objects.get(id=request.POST['id_op'])
    orden.estado = Tipo.objects.get(nombre='En proveedor')
    orden.save()
    return JsonResponse({'mensaje': 'ok'})
