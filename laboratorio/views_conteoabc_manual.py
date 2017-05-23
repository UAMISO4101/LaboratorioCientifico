# coding=utf-8

import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from laboratorio import views_busqueda_producto
from django.db.models import Q
from django.db import connection
from datetime import datetime, timedelta
from laboratorio.modelos_vista import Convertidor, json_default, ConteoABCVista, DetalleProductoVista
from laboratorio.models import Tipo, Producto, Bodega, ConteoInventario, DetalleProductos


@csrf_exempt
def ir_conteosabc(request):
    return render(request, "laboratorio/ver_conteos_abc.html")

@csrf_exempt
def ir_obtenerconteoabc(request):
    return render(request, "laboratorio/conteoabc_fisico.html")


"""Metodo obtener conteos abc.
HU: EC-LCINV-20: Adicionar conteo abc manual
Sirve para obtener los conteos de inventario abc que tiene el sistema
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtener_conteos_abc(request):
    qs = ConteoInventario.objects.all()
    listaConteos = []
    for conteo in qs:
        c = ConteoABCVista()
        c.id = conteo.id
        if conteo.usuario_creacion != None:
            c.nombreUsuarioCreacion = conteo.usuario_creacion.first_name + " " + conteo.usuario_creacion.last_name
        else:
            c.nombreUsuarioCreacion = " "
        c.estado = conteo.estado.nombre
        dh = timedelta(hours=5)
        c.fechaCreacion = (conteo.fecha_creacion - dh).strftime("%c")
        listaConteos.append(c)
    json_string = json.dumps(listaConteos, cls=Convertidor)
    return JsonResponse(json_string, safe=False)

"""Metodo obtener conteo abc.
HU: EC-LCINV-20: Adicionar conteo abc manual
Sirve para obtener detalle de un conteo de inventario abc que tiene el sistema
request, es la peticion dada por el usuario
return, formato json con los usuarios
"""
@csrf_exempt
def obtener_conteo_abc(request):
    qs = DetalleProductos.objects.filter(conteoinventario=request.GET['id_conteo']).order_by('producto','id')
    listaConteos = []
    ver_btn_ajuste = False
    if qs.exists():
        for det_producto in qs:
            detalle = DetalleProductoVista()
            detalle.idDetalle = det_producto.id
            if det_producto.producto is not None:
                detalle.nombreProducto = det_producto.producto.nombre
            if det_producto.bodega is not None:
                detalle.nombreBodega = det_producto.bodega.nombre
                detalle.nivel = det_producto.nivel
                detalle.seccion = det_producto.seccion
            detalle.cantidad = int(det_producto.cantidad_contada)
            detalle.diferencia_cantidad = det_producto.diferencia_cantidad
            if det_producto.unidad_medida is not None:
               detalle.unidadMedida = det_producto.unidad_medida.nombre
            listaConteos.append(detalle)
            if not ver_btn_ajuste and (det_producto.diferencia_cantidad == None or det_producto.diferencia_cantidad != 0):
                ver_btn_ajuste = True

        if ver_btn_ajuste:
            listaConteos.__getitem__(0).ver_btn_ajuste = "1"
        else:
            listaConteos.__getitem__(0).ver_btn_ajuste = "0"

        detalles_prod = DetalleProductos.objects.filter(conteoinventario=det_producto.conteoinventario)
        cantidadNone = detalles_prod.filter(cantidad_fisica=None).count()
        cantidadCero = detalles_prod.filter(diferencia_cantidad=0).count()
        ver_msj_cerrada = "0"
        if cantidadNone == 0:
            cont_inv = ConteoInventario.objects.filter(id=det_producto.conteoinventario.id).first()
            if cantidadCero != detalles_prod.count():
                cont_inv.estado = Tipo.objects.get(grupo = "STATUSCONTEO",nombre__contains="Ajustes")
            else:
                cont_inv.estado = Tipo.objects.get(grupo = "STATUSCONTEO",nombre__contains="Cerrada")
                ver_msj_cerrada = "1"
            cont_inv.save()
        else:
            listaConteos.__getitem__(0).ver_btn_ajuste = "0"
        listaConteos.__getitem__(0).ver_msj_cerrada = ver_msj_cerrada
    json_string = json.dumps(listaConteos, cls=Convertidor)
    return JsonResponse(json_string, safe=False)

"""Metodo actualizar conteo fisico.
HU: EC-LCINV-20: Adicionar conteo abc manual
Sirve para actualizar el conteo manual de un item para determinado producto
request, es la peticion dada por el usuario
return, formato json con la respuesta si es exceso o defecto
"""
@csrf_exempt
def actualizar_conteo_fisico(request):
    diferencia_cantidad = 0
    tipo_diferencia = "-"
    ver_btn_ajuste = "0"
    ver_msj_cerrada = "0"

    # Capturar el valor de los campos
    if request.method == 'POST':
        qs = DetalleProductos.objects.filter(id=request.POST['id_detalle_conteo'])
        if qs.exists():
            det_producto = qs.first()
            if request.POST['cantidad_fisica'] != None and request.POST['cantidad_fisica'] != '':
                cantidad_fisica = int(request.POST['cantidad_fisica'])
                det_producto.cantidad_fisica = cantidad_fisica
                if det_producto.cantidad_contada < det_producto.cantidad_fisica:
                    det_producto.tipo_diferencia = Tipo.objects.get(nombre__contains="Exceso")
                    det_producto.diferencia_cantidad = det_producto.cantidad_fisica - det_producto.cantidad_contada
                elif det_producto.cantidad_contada > det_producto.cantidad_fisica:
                    det_producto.tipo_diferencia = Tipo.objects.get(nombre__contains="Defecto")
                    det_producto.diferencia_cantidad = det_producto.cantidad_contada - det_producto.cantidad_fisica
                else:
                    det_producto.tipo_diferencia = Tipo.objects.get(nombre__contains="-")
                    det_producto.diferencia_cantidad = 0

                det_producto.save()
                detalles_prod = DetalleProductos.objects.filter(conteoinventario=det_producto.conteoinventario)
                cantidadNone = detalles_prod.filter(cantidad_fisica = None).count()
                cantidadCero = detalles_prod.filter(diferencia_cantidad = 0).count()
                if cantidadNone == 0:
                    cont_inv = ConteoInventario.objects.filter(id=det_producto.conteoinventario.id).first()
                    if cantidadCero != detalles_prod.count():
                        ver_btn_ajuste = "1"
                        cont_inv.estado = Tipo.objects.get(grupo = "STATUSCONTEO", nombre__contains="Ajustes")
                    else:
                        cont_inv.estado = Tipo.objects.get(grupo = "STATUSCONTEO", nombre__contains="Cerrada")
                        ver_msj_cerrada = "1"
                    cont_inv.save()
            strDiferencia = '0'
            if det_producto.diferencia_cantidad != None:
                strDiferencia = str(det_producto.diferencia_cantidad)
            unidad = ""
            if det_producto.unidad_medida != None:
                unidad =  det_producto.unidad_medida.nombre
            diferencia_cantidad = strDiferencia + " " + unidad
            tipo_diferencia = det_producto.tipo_diferencia.nombre

    return JsonResponse({"diferencia_cantidad": diferencia_cantidad.strip(),"tipo_diferencia": tipo_diferencia, "ver_btn_ajuste": ver_btn_ajuste, "ver_msj_cerrada":ver_msj_cerrada})
