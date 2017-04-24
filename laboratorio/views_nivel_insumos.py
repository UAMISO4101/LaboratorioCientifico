from __future__ import division
from decimal import Decimal

import sys

from datetime import datetime, timedelta
from django.core import serializers
from django.core.serializers import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from laboratorio.models import Producto, ProductosEnBodega, TransaccionInventario, Tipo

def ir_nivel_insumos(request, id=1):
    return render(request, "laboratorio/nivelInsumos.html")

def calcularStockSeguridad(frecuencia_minima, cantidad_uso, tiempo, numero_minimo_veces):
    if frecuencia_minima == "Continua":
        #Muchas veces al dia
        return numero_minimo_veces*cantidad_uso*tiempo
    elif frecuencia_minima == "Frecuente":
        #Al menos una vez al dia
        return cantidad_uso*tiempo
    elif frecuencia_minima == "Ocasional":
        #Al menos una vez a la semana
        diario = cantidad_uso/7
        return diario*tiempo
    elif frecuencia_minima == "PocoUsual":
        #Al menos una vez al mes (aproximando a 30 dias)
        diario = cantidad_uso/30
        return diario*tiempo
    elif frecuencia_minima == "Rara":
        #Unas pocas veces al anio
        suma = cantidad_uso*numero_minimo_veces
        diario = suma/365
        return diario*tiempo
    elif frecuencia_minima == "MuyRara":
        #Al menos una vez al anio
        diario = cantidad_uso/365
        return diario*tiempo

def calcularPuntoPedido(stock_seguridad, frecuencia_media, cantidad_media, tiempo, numero_medio_veces):
    val = calcularStockSeguridad(frecuencia_media, cantidad_media, tiempo,numero_medio_veces)
    return val + stock_seguridad

def nivel_insumo_tabla(pk_producto, punto_pedido):
    listress = []
    valRojoMax = (Decimal(punto_pedido)*Decimal(0.25))+Decimal(punto_pedido)
    valNaranjaMax = (Decimal(punto_pedido)*Decimal(0.5))+Decimal(punto_pedido)
    listres = calculo_niveles(pk_producto)
    nivelProveedor = listres[0]
    nivelPerdidaDesperdicio = listres[1]
    nivelExperimento = listres[2]
    nivelDevolucion = listres[3]
    nivelPaso = listres[4]
    nivel_actual =(nivelProveedor-nivelPerdidaDesperdicio-nivelDevolucion-nivelExperimento)
    print >> sys.stdout, 'nivel actual '+ str(nivel_actual)
    if nivel_actual == 0 or nivel_actual < Decimal(punto_pedido):
        listress.append(-1)
        listress.append(nivel_actual)
    elif nivel_actual >= Decimal(punto_pedido) and nivel_actual<valRojoMax:
        listress.append(0)
        listress.append(nivel_actual)
    elif nivel_actual>=valRojoMax and nivel_actual<valNaranjaMax:
        listress.append(1)
        listress.append(nivel_actual)
    elif nivel_actual>=valNaranjaMax:
        listress.append(2)
        listress.append(nivel_actual)
    return listress

@csrf_exempt
def recalcular_nivel_actual_(request):
    if request.method == 'GET':
        pk_producto = request.GET['id']
        listres = calculo_niveles(pk_producto)
        nivelProveedor = listres[0]
        nivelPerdidaDesperdicio = listres[1]
        nivelExperimento = listres[2]
        nivelDevolucion = listres[3]
        nivelPaso = listres[4]

        total = nivelProveedor
        print >> sys.stdout, 'proveedor'+ str(nivelProveedor)
        print >> sys.stdout, 'perdida'+ str(nivelPerdidaDesperdicio)
        print >> sys.stdout, 'experimento'+str(nivelExperimento)
        print >> sys.stdout, 'devolucion'+ str(nivelDevolucion)
        print >> sys.stdout, 'paso'+ str(nivelPaso)
        print >> sys.stdout, 'total ' + str(total)
        if total!= 0:
            n1 = ((nivelProveedor-nivelPerdidaDesperdicio-nivelDevolucion-nivelExperimento)/total)*100
            n2 = (nivelPerdidaDesperdicio/total)*100
            n3 = (nivelExperimento/total) * 100
            n4 = (nivelDevolucion/total) * 100
            n5 = (nivelPaso/total)*100
        else:
            n1 = 0
            n2 = 0
            n3 = 0
            n4 = 0
            n5 = 0
        nombre = str(Producto.objects.get(id=pk_producto).nombre)
        return JsonResponse({'proveedor': n1, 'perdida': n2, 'experimento': n3,
                             'devolucion': n4, 'paso': n5, 'nombre': nombre})

def calculo_niveles(pk_producto):
    listres = []
    nivelProveedor = 0
    nivelPerdidaDesperdicio = 0
    nivelExperimento = 0
    nivelDevolucion = 0
    nivelPaso = 0
    tipo1 = Tipo.objects.get(nombre="Recepcion de Proveedor")
    tipo2 = Tipo.objects.get(nombre="Mover por perdida o desperdicio")
    tipo3 = Tipo.objects.get(nombre="Traslado a experimento")
    tipo4 = Tipo.objects.get(nombre="Devolucion a proveedor")
    tipo5 = Tipo.objects.get(nombre="Paso entre bodegas")
    tranRecepcion = TransaccionInventario.objects.filter(producto=pk_producto).filter(tipo=tipo1.id)
    if len(tranRecepcion) >= 1:
        for tran in tranRecepcion:
            nivelProveedor += tran.cantidad
    else:
        nivelProveedor = 0
    tranRecepcion = TransaccionInventario.objects.filter(producto=pk_producto).filter(tipo=tipo2.id)
    if len(tranRecepcion) >= 1:
        for tran in tranRecepcion:
            nivelPerdidaDesperdicio += tran.cantidad
    else:
        nivelPerdidaDesperdicio = 0
    tranRecepcion = TransaccionInventario.objects.filter(producto=pk_producto).filter(tipo=tipo3.id)
    if len(tranRecepcion) >= 1:
        for tran in tranRecepcion:
            if tran.producto_bodega_origen.bodega.tipo_bodega.nombre == "Experimento":
                nivelExperimento = nivelExperimento
            else:
                nivelExperimento += tran.cantidad
    else:
        nivelExperimento = 0
    tranRecepcion = TransaccionInventario.objects.filter(producto=pk_producto).filter(tipo=tipo4.id)
    if len(tranRecepcion) >= 1:
        for tran in tranRecepcion:
            nivelDevolucion += tran.cantidad
    else:
        nivelDevolucion = 0
    tranRecepcion = TransaccionInventario.objects.filter(producto=pk_producto).filter(tipo=tipo5.id)
    if len(tranRecepcion) >= 1:
        for tran in tranRecepcion:
            if tran.producto_bodega_origen.bodega.tipo_bodega.nombre == "Desperdicio":
                nivelPaso+=tran.cantidad
                nivelProveedor+=tran.cantidad
            elif tran.producto_bodega_origen.bodega.tipo_bodega.nombre == "Experimento":
                nivelPaso+=tran.cantidad
                nivelProveedor+=tran.cantidad
            elif tran.producto_bodega_origen.bodega.tipo_bodega.nombre == "Nevera":
                nivelPaso+=tran.cantidad
    else:
        nivelPaso = 0
    listres.append(nivelProveedor)
    listres.append(nivelPerdidaDesperdicio)
    listres.append(nivelExperimento)
    listres.append(nivelDevolucion)
    listres.append(nivelPaso)
    return listres

@csrf_exempt
def historial_nivel(request):
    if request.method == 'GET':
        pk_producto = request.GET['id']
        tipo1 = Tipo.objects.get(nombre="Recepcion de Proveedor")
        tipo2 = Tipo.objects.get(nombre="Mover por perdida o desperdicio")
        tipo3 = Tipo.objects.get(nombre="Traslado a experimento")
        tipo4 = Tipo.objects.get(nombre="Devolucion a proveedor")
        tipo5 = Tipo.objects.get(nombre="Paso entre bodegas")
        tranLabel = TransaccionInventario.objects.filter(producto=pk_producto).order_by('fecha_ejecucion')
        listLabel = []
        listTipo1 = []

        nivelActual = 0
        i = 0
        ultimaTransicion = None
        for tran in tranLabel:
            print >> sys.stdout, str(tran.fecha_ejecucion)+ ' '+str(tran.tipo.nombre)+' '+str(tran.cantidad) + ' i'+str(i)
            listLabel.append(str(tran.fecha_ejecucion.strftime('%Y-%m-%d')))
            if tran.tipo.nombre == tipo1.nombre:
                nivelActual+=tran.cantidad
                listTipo1.append(nivelActual)
            elif tran.tipo.nombre == tipo3.nombre:
                if tran.producto_bodega_origen.bodega.tipo_bodega.nombre == "Experimento":
                    nivelActual=nivelActual
                else:
                    nivelActual-=tran.cantidad
                listTipo1.append(nivelActual)
            elif tran.tipo.nombre ==  tipo2.nombre or tran.tipo.nombre == tipo4.nombre:
                nivelActual-=tran.cantidad
                listTipo1.append(nivelActual)
            elif tran.tipo.nombre == tipo5.nombre:
                if tran.producto_bodega_origen.bodega.tipo_bodega.nombre == "Desperdicio":
                    nivelActual += tran.cantidad
                elif tran.producto_bodega_origen.bodega.tipo_bodega.nombre == "Experimento":
                    nivelActual += tran.cantidad
                elif tran.producto_bodega_origen.bodega.tipo_bodega.nombre == "Nevera":
                    nivelActual = nivelActual
                listTipo1.append(nivelActual)
            if i == len(tranLabel) - 1:
                ultimaTransicion = tran
            else:
                i += 1
        nombre = str(Producto.objects.get(id=pk_producto).unidad_medida.nombre)

        resDate = "Ultima transaccion ejecutada "+ str(ultimaTransicion.fecha_ejecucion.strftime('%Y-%m-%d %H:%m'))
        return JsonResponse([listLabel, listTipo1, max(listTipo1), nombre, resDate], safe=False)