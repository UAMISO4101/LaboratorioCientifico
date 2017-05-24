# coding=utf-8

import json
import time
import sys
from django.core import serializers
from datetime import datetime, timedelta
from decimal import Decimal
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from laboratorio import views_nivel_insumos
from laboratorio.modelos_vista import BodegaVista, Convertidor, TransaccionVista, json_default
from laboratorio.models import Tipo, Usuario, Bodega, TransaccionInventario, ProductosEnBodega, Producto, \
    ProductoReposicionPendiente
from django.shortcuts import render

def ir_crear_transaccion(request):
    return render(request,"laboratorio/crearTransaccion.html")

def ir_transacciones(request):
    return render(request,"laboratorio/transacciones.html")

@csrf_exempt
def obtenerTransacciones(request):
    qs = TransaccionInventario.objects.all()
    listaTransacciones = []
    for transaccion in qs:
        trx = TransaccionVista()
        trx.id = transaccion.id
        trx.tipo = transaccion.tipo.nombre
        trx.bodega_origen = transaccion.bodega_origen.nombre
        trx.nivel_origen = transaccion.nivel_origen
        trx.seccion_origen = transaccion.seccion_origen
        trx.bodega_destino = transaccion.bodega_destino.nombre
        trx.nivel_destino = transaccion.nivel_destino
        trx.seccion_destino = transaccion.seccion_destino
        trx.producto = transaccion.producto.nombre
        trx.cantidad = transaccion.cantidad
        trx.unidad_medida = transaccion.unidad_medida.nombre
        trx.estado = transaccion.estado.nombre
        trx.fecha_creacion = transaccion.fecha_creacion
        trx.fecha_ejecucion = transaccion.fecha_ejecucion
        trx.comentarios = transaccion.comentarios
        trx.usuario = transaccion.usuario
        #bod.responsable = bodega.usuario.first_name + " " + bodega.usuario.last_name
        listaTransacciones.append(trx)
    json_string = json.dumps(listaTransacciones, cls=Convertidor, ensure_ascii=False, default=json_default)
    return JsonResponse(json_string, safe=False)

#HU-LCINV-13
#GZ
#Obtiene la lista de transacciones para mostrarla en la tabla del UI
@csrf_exempt
def obtenerTransaccion(request):
    time.sleep(0.3)
    qs = TransaccionInventario.objects.filter(id=request.GET['id_transaccion'])
    qs_json = serializers.serialize('json', qs)
    struct = json.loads(qs_json)
    json_bodega = json.dumps(struct[0])
    return JsonResponse({"transaccion": json_bodega})


#HU-LCINV-13
#GZ
#Crea una transaccion de inventario:
#Recibe bodega origen con localizacion (Nivel, Seccion)
#Bodega destino con localizacion (Nivel, Seccion)
#Producto y cantidad a mover

@csrf_exempt
def crear_transaccion(request):
    if request.method == 'POST':
        json_tran = json.loads(request.body)
        print >> sys.stdout, "Prod" + json_tran['producto']
        print >> sys.stdout, "PRODProd" + json_tran['producto_bodega_origen']
        transaccion = TransaccionInventario(
            tipo=Tipo.objects.get(pk=json_tran['tipo']),
            bodega_origen= Bodega.objects.get(pk=json_tran['bodega_origen']),
            nivel_origen=json_tran['nivel_origen'],
            seccion_origen=json_tran['seccion_origen'],
            bodega_destino = Bodega.objects.get(pk=json_tran['bodega_destino']),
            nivel_destino=json_tran['nivel_destino'],
            seccion_destino=json_tran['seccion_destino'],
            producto_bodega_origen = ProductosEnBodega.objects.filter(id=json_tran['producto_bodega_origen']).first(),
            producto=Producto.objects.get(pk=json_tran['producto']),
            cantidad=json_tran['cantidad'],
            unidad_medida=Tipo.objects.get(nombre=json_tran['unidad_medida'], grupo='MEDIDAPRODUCTO'),
            estado=Tipo.objects.get(pk=Tipo.objects.filter(nombre='Ejecutada', grupo='STATUSTRX').first().id),
            fecha_creacion=datetime.now(),
            fecha_ejecucion=datetime.now(),
            usuario=Usuario.objects.get(pk=1),
            comentarios=json_tran['comentarios']
        )
        ejecutar_transaccion(transaccion, request=request)
        transaccion.save()
        res = lanzar_notificacionOrdenReposicion(pk_producto=json_tran['producto'])
        tran_json = json.loads(serializers.serialize('json', [transaccion]))
        if len(res) != 0:
            # se lanza notificacion de reposicion, na, pp
            request.session['producto_id'] = transaccion.producto.id
            print >> sys.stdout, 'ID PRODUCTO '+str(request.session.get('producto_id', None))
            return JsonResponse({'tran': tran_json, 'res0': res[0], 'res1': res[1]}, safe=False)
        else:
            return JsonResponse({'tran': tran_json}, safe=False)


# HU-LCINV-13
# GZ
#Ejecuta la transaccion de inventario: Afecta las cantidades de producto por un movimento pedido
#Resta de la bodega origen y suma o crea registro en la bodega destino

@csrf_exempt
def ejecutar_transaccion(transaccion, request):

        if transaccion.tipo.nombre != "Recepcion de Proveedor" and \
                (transaccion.tipo.nombre != "Ajuste Inventario" or \
                (transaccion.tipo.nombre == "Ajuste Inventario" and transaccion.producto_bodega_origen != None)):
                producto_bodega_origen = ProductosEnBodega.objects.get(pk=transaccion.producto_bodega_origen.pk)
                producto_bodega_origen.cantidad = int(producto_bodega_origen.cantidad) - int(transaccion.cantidad)
                producto = producto_bodega_origen.producto
        else:
            producto = transaccion.producto

        producto_bodega_destino_list = ProductosEnBodega.objects.filter(bodega=transaccion.bodega_destino)
        producto_bodega_destino_list = producto_bodega_destino_list.filter(producto=transaccion.producto)
        producto_bodega_destino_list = producto_bodega_destino_list.filter(nivel=transaccion.nivel_destino)
        producto_bodega_destino_list = producto_bodega_destino_list.filter(seccion=transaccion.seccion_destino)

        if producto_bodega_destino_list.exists():
            producto_bodega_destino = producto_bodega_destino_list.first()
            producto_bodega_destino.cantidad = int(producto_bodega_destino.cantidad) + int(transaccion.cantidad)
        else:
            producto_bodega_destino = ProductosEnBodega(
                                    bodega=transaccion.bodega_destino,
                                    producto = producto,
                                    nivel = transaccion.nivel_destino,
                                    seccion = transaccion.seccion_destino,
                                    cantidad = transaccion.cantidad,
                                    unidad_medida=transaccion.unidad_medida

            )

        producto_bodega_destino.save()
        transaccion.fecha_ejecucion=datetime.now()
        transaccion.producto_bodega_destino = producto_bodega_destino
        transaccion.estado = Tipo.objects.get(pk=Tipo.objects.filter(nombre='Ejecutada').first().id)
        transaccion.save()
        if transaccion.tipo.nombre != "Recepcion de Proveedor" and \
                (transaccion.tipo.nombre != "Ajuste Inventario" or \
                (transaccion.tipo.nombre == "Ajuste Inventario" and transaccion.producto_bodega_origen != None)):
                producto_bodega_origen.save()
        else:
            if ProductoReposicionPendiente.objects.filter(producto_id=transaccion.producto_id).exists() == True:
                ProductoReposicionPendiente.objects.filter(producto_id=transaccion.producto_id).delete()
            if request.session.get('orden_pedido_id', None) != None:
                del request.session['orden_pedido_id']
            if request.session.get('producto_id', None) != None:
                del request.session['producto_id']



def lanzar_notificacionOrdenReposicion(pk_producto):

    notifi = []
    producto = Producto.objects.get(id=pk_producto)
    punto_pedido = producto.punto_pedido
    listres = views_nivel_insumos.nivel_insumo_tabla(pk_producto=pk_producto, punto_pedido=punto_pedido)
    codigo_color = listres[0]
    if codigo_color <= 0:
        notifi.append(listres[1])
        notifi.append(punto_pedido)
    return notifi