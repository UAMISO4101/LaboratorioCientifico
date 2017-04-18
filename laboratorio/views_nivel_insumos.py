from decimal import Decimal

import sys
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from laboratorio.models import Producto, ProductosEnBodega

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
        producto = Producto.objects.get(id=pk_producto)
        inventario_inicial = producto.unidadesExistentes*producto.unidad_unitaria
        print >> sys.stdout, 'inventarioInicial '+str(inventario_inicial)
        suma = 0
        producto_bodega_list = ProductosEnBodega.objects.filter(producto_id=pk_producto)
        for pro in producto_bodega_list:
            print >> sys.stdout, 'cantidad en bogeda '+ pro.bodega.nombre + ' '+ str(pro.cantidad)
            suma += pro.cantidad
        disponible = ((inventario_inicial-suma)/inventario_inicial)*100
        suma = (suma/inventario_inicial)*100
        return JsonResponse({'disponible': disponible, 'enUso': suma})

