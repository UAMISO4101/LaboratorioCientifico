from __future__ import division
from decimal import Decimal

import sys

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

def nivel_insumo(punto_pedido, nivel_actual):
    valRojoMax = (punto_pedido*0.25)+punto_pedido
    valNaranjaMax = (punto_pedido*0.5)+punto_pedido

    if nivel_actual < punto_pedido:
        return -1
    elif nivel_actual >= punto_pedido and nivel_actual<valRojoMax:
        return  0
    elif nivel_actual>=valRojoMax and nivel_actual<valNaranjaMax:
        return 1
    elif nivel_actual>=valNaranjaMax:
        return 2

@csrf_exempt
def recalcular_nivel_actual_(request):
    if request.method == 'GET':
        pk_producto = request.GET['id']
        tipo1 = Tipo.objects.get(nombre="Recepcion de Proveedor")
        tipo2 = Tipo.objects.get(nombre="Mover por perdida o desperdicio")
        tipo3 = Tipo.objects.get(nombre="Traslado a experimento")
        tipo4 = Tipo.objects.get(nombre="Devolucion a proveedor")
        tipo5 = Tipo.objects.get(nombre="Paso entre bodegas")
        #Transacciones de recepcion de proveedor, se consulta la cantidad en bodega origen y se efectua
        #la sumatoria para conocer el nivel de inventario del producto actual
        nivelProveedor = 0
        nivelPerdidaDesperdicio = 0
        nivelExperimento = 0
        nivelDevolucion = 0
        nivelPaso = 0
        tranRecepcion = TransaccionInventario.objects.filter(producto=pk_producto).filter(tipo=tipo1.id)
        if len(tranRecepcion)>=1:
            for tran in tranRecepcion:
                nivelProveedor+=tran.cantidad
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
                nivelPaso += tran.cantidad
        else:
            nivelPaso = 0
        total = nivelProveedor+nivelPerdidaDesperdicio+nivelExperimento+nivelDevolucion+nivelPaso
        print >> sys.stdout, 'total ' + str(total)
        if total!= 0:
            n1 = (nivelProveedor/total)*100
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
        return JsonResponse({'proveedor': n1, 'perdida': n2, 'experimento': n3,
                             'devolucion': n4, 'paso': n5})

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
        tranInvTipo1= TransaccionInventario.objects.filter(producto=pk_producto).filter(tipo=tipo1.id).order_by('fecha_ejecucion')
        tranInvTipo2= TransaccionInventario.objects.filter(producto=pk_producto).filter(tipo=tipo2.id).order_by('fecha_ejecucion')
        tranInvTipo3= TransaccionInventario.objects.filter(producto=pk_producto).filter(tipo=tipo3.id).order_by('fecha_ejecucion')
        tranInvTipo4= TransaccionInventario.objects.filter(producto=pk_producto).filter(tipo=tipo4.id).order_by('fecha_ejecucion')
        tranInvTipo5= TransaccionInventario.objects.filter(producto=pk_producto).filter(tipo=tipo5.id).order_by('fecha_ejecucion')
        listLabel = []
        listTipo1 = []
        listTipo2 = []
        listTipo3 = []
        listTipo4 = []
        listTipo5 = []

        for tran in tranLabel:
            print >> sys.stdout, str(tran.fecha_ejecucion)+ ' '+str(tran.tipo.nombre)+' '+str(tran.cantidad)
            listLabel.append(str(tran.fecha_ejecucion))

        for tran in tranInvTipo1:
            print >> sys.stdout, 'tipo1 '+str(tran.cantidad)
            listTipo1.append(str(tran.cantidad))

        for tran in tranInvTipo2:
            print >> sys.stdout, 'tipo2 ' + str(tran.cantidad)
            listTipo2.append(str(tran.cantidad))

        for tran in tranInvTipo3:
            print >> sys.stdout, 'tipo3 ' + str(tran.cantidad)
            listTipo3.append(str(tran.cantidad))

        for tran in tranInvTipo4:
            print >> sys.stdout, 'tipo4 ' + str(tran.cantidad)
            listTipo4.append(str(tran.cantidad))

        for tran in tranInvTipo5:
            print >> sys.stdout, 'tipo5 ' + str(tran.cantidad)
            listTipo5.append(str(tran.cantidad))

        return JsonResponse([listLabel, listTipo1, listTipo2, listTipo3, listTipo4, listTipo5], safe=False)