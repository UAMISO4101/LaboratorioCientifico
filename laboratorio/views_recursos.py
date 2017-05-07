# coding=utf-8

import json
import time
import sys
from django.core import serializers
from datetime import datetime, timedelta
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from laboratorio import views_nivel_insumos
from laboratorio.modelos_vista import BodegaVista, Convertidor, ProductoVista
from laboratorio.models import Tipo, Usuario, Bodega, Producto
from django.shortcuts import render

#HU: SA-LCINV-3
#SA
#Metodo a navegar al menu de registro de materiales e insumos
def ir_recursos(request):
    return render(request, "laboratorio/recursos.html")
#HU: SA-LCINV-3
#SA
#Metodo a navegar al formulario de registro de insumos
def ir_regitrarInsumos(request):
    return render(request, "laboratorio/registroInsumos.html")
#HU: SA-LCINV-3
#SA
#Metodo a navegar a la lista de recursos
def ir_ver_recursos(request):
    return render(request, "laboratorio/verRecursos.html")
#HU: SA-LCINV-3
#SA
#Metodo a navegar al formulario de edicion de insumos
def ir_editarRecurso(request, recurso_id=1):
    return render(request, "laboratorio/edicionInsumos.html")

#HU: SA-LCINV-3
#SA
#Metodo que representa el servicio REST que hace el registro de un nuevo recurso (Insumo/Reactivo)
#Recibe los campos ingresados en el formulario de registro de recursos
#Si no hay otro recurso con el mismo codigo o nombre se hace el registro y se retorna un mensaje ok en formato JSON
#En caso contrario se indica el respectivo mensaje de error en formato JSON
@csrf_exempt
def registrarInsumoReactivo(request):
    mensaje = ""
    dosLugares = Decimal('00.01')
    errNum = False
    if request.method == 'POST':
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        if request.POST['valor'] == "":
            valor = 0
        else:
            valor = int(request.POST['valor'])
        if request.POST['unidades'] == "":
            unidadesExistentes = 0
        else:
            unidadesExistentes = int(request.POST['unidades'])
        clasificacion = request.POST['clasificacion']
        if request.POST['cantidad'] == "":
            unitaria = 0.0
        else:
            unitaria = Decimal(request.POST['cantidad'])
        imageFile = request.FILES.get('imageFile', None)
        frecuencia_media = request.POST['frecuencia_media']
        if frecuencia_media == "Continua" or frecuencia_media == "Rara":
            numero_medio_veces = int(request.POST['numero_medio_promedio'])
            if int(numero_medio_veces) <= 0:
                errNum = True
        else:
            numero_medio_veces = 0
        if request.POST['cantidad_media'] == "":
            cantidad_media = 0.0
        else:
            cantidad_media = Decimal(request.POST['cantidad_media'])
        frecuencia_minima =  request.POST['frecuencia_minima']
        if frecuencia_minima == "Continua" or frecuencia_minima == "Rara":
            numero_minimo_veces = int(request.POST['numero_minimo_promedio'])
            if int(numero_minimo_veces) <= 0:
                errNum = True
        else:
            numero_minimo_veces = 0
        if request.POST['tiempo'] == "":
            tiempo = 0
        else:
            tiempo = int(request.POST['tiempo'])
        if codigo != "" and nombre != "" and descripcion != "" and valor != 0 and unidadesExistentes != 0 and unitaria != 0 and imageFile != None and request.POST['cantidad'] != "" and request.POST['proveedor'] != "" and cantidad_media != 0.0 and tiempo != 0 and errNum == False:
            if Producto.objects.filter(codigo=codigo).first() != None or Producto.objects.filter(nombre=nombre).first() !=None:
                mensaje = "El insumo/reactivo con el codigo o nombre ingresado ya existe."
            else:
                proveedor = Usuario.objects.filter(id=request.POST['proveedor']).first()
                if proveedor.first_name == "Interno (recurso propio)":
                    frecuencia_media = "NA"
                    frecuencia_minima = "NA"
                    cantidad_media = 0.0
                    tiempo = 0
                    stock_seguridad = 0.0
                    punto_pedido = 0.0

                else:
                    stock_seguridad = views_nivel_insumos.calcularStockSeguridad(frecuencia_minima, cantidad_media, tiempo, numero_minimo_veces)
                    punto_pedido = views_nivel_insumos.calcularPuntoPedido(stock_seguridad, frecuencia_media, cantidad_media, tiempo, numero_medio_veces)

                #Es un producto con un codigo y un nombre nuevos
                producto = Producto(codigo=codigo,
                                    nombre=nombre,
                                    descripcion=descripcion,
                                    valorUnitario=valor,
                                    unidadesExistentes=unidadesExistentes,
                                    clasificacion=clasificacion,
                                    unidad_medida=Tipo.objects.filter(id=request.POST['medida']).first(),
                                    unidad_unitaria=unitaria,
                                    imageFile=imageFile,
                                    proveedor=proveedor,
                                    frecuencia_media_uso=frecuencia_media,
                                    cantidad_media_uso=cantidad_media,
                                    frecuencia_minima_uso=frecuencia_minima,
                                    tiempo_reaprovisionamiento=tiempo,
                                    stock_seguridad=stock_seguridad,
                                    punto_pedido=punto_pedido)

                producto.unidad_unitaria.quantize(dosLugares, 'ROUND_DOWN')
                producto.cantidad_media_uso.quantize(dosLugares, 'ROUND_DOWN')
                producto.stock_seguridad.quantize(dosLugares, 'ROUND_DOWN')
                producto.punto_pedido.quantize(dosLugares, 'ROUND_DOWN')
                producto.save()
                mensaje = "ok"
        else:
            mensaje = "Todos los campos deben estar debidamente diligenciados"

    return JsonResponse({"mensaje":mensaje})

#HU: SA-LCINV-3
#SA
#Metodo que representa el servicio REST para retornar todos los recursos/productos guardados
#en la base de datos en un arreglo con formato JSON
@csrf_exempt
def obtenerRecursos(request):
    qs = Producto.objects.all()
    listaProductos = []
    for producto in qs:
        prod = ProductoVista()
        prod.id = producto.id
        prod.codigo = producto.codigo
        prod.nombre = producto.nombre
        prod.descripcion = producto.descripcion
        prod.valorUnitario = str(producto.valorUnitario)
        prod.unidadesExistentes = str(producto.unidadesExistentes)
        prod.clasificacion = producto.get_clasificacion_display()
        prod.unidad_medida = producto.unidad_medida.nombre
        prod.unidad_unitaria = str(producto.unidad_unitaria)
        prod.imageFile = str(producto.imageFile)
        prod.proveedor = producto.proveedor.first_name
        codigo_color = views_nivel_insumos.nivel_insumo_tabla(producto.id, producto.punto_pedido)
        prod.codigo_color = str(codigo_color[0])
        prod.punto_pedido = str(producto.punto_pedido)
        prod.nivel_actual = str(codigo_color[1])
        print>> sys.stdout, 'punto_pedido '+ producto.nombre + ' '+ str(producto.punto_pedido)+ ' nivel actual '+ str(codigo_color[1])
        listaProductos.append(prod)
    json_string = json.dumps(listaProductos, cls=Convertidor)
    return JsonResponse(json_string, safe=False)

#HU: SA-LCINV-3
#SA
#Metodo que representa el servicio REST para retornar un recurso en formato JSON cuando en el
#request de la peticion llega el id de ese recurso
@csrf_exempt
def obtenerRecurso(request):
    time.sleep(0.3)
    qs = Producto.objects.filter(id=request.GET['recurso_id'])
    qs_json = serializers.serialize('json', qs)
    struct = json.loads(qs_json)
    json_recurso = json.dumps(struct[0])
    return JsonResponse({"producto": json_recurso})

#HU: SA-LCINV-3
#SA
#Metodo que representa el servicio REST para guardar la edicion que se ha hecho de un recurso
#Solo se guardara la edicion si no se presentan conflictos de codigo o nombre con otros recursos
#y si estan todos los campos completos a excepcion de la imagen que es opcional, se retorna un
#mensaje en formato JSON
@csrf_exempt
def guardarEdicionInsumo(request):

    mensaje = ""
    errNum = False
    if request.method == 'POST':
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        if request.POST['valor'] == "":
            valor = 0
        else:
            valor = int(request.POST['valor'])
        if request.POST['unidades'] == "":
            unidadesExistentes = 0
        else:
            unidadesExistentes = int(request.POST['unidades'])
        clasificacion = request.POST['clasificacion']
        if request.POST['cantidad'] == "":
            unitaria = 0.0
        else:
            unitaria = Decimal(request.POST['cantidad'])
        clasificacion = request.POST['clasificacion']
        imageFile = request.FILES.get('imageFile',None)
        frecuencia_media = request.POST['frecuencia_media']
        if frecuencia_media == "Continua" or frecuencia_media == "Rara":
            numero_medio_veces = int(request.POST['numero_medio_promedio'])
            if int(numero_medio_veces) <= 0:
                errNum = True
        else:
            numero_medio_veces = 0
        if request.POST['cantidad_media'] == "":
            cantidad_media = 0.0
        else:
            cantidad_media = Decimal(request.POST['cantidad_media'])
        frecuencia_minima = request.POST['frecuencia_minima']
        if frecuencia_minima == "Continua" or frecuencia_minima == "Rara":
            numero_minimo_veces = int(request.POST['numero_minimo_promedio'])
            if int(numero_minimo_veces) <= 0:
                errNum = True
        else:
            numero_minimo_veces = 0
        if request.POST['tiempo'] == "":
            tiempo = 0
        else:
            tiempo = int(request.POST['tiempo'])
        producto = Producto.objects.filter(id=int(request.POST['id_producto_guardado'])).first()


        modificacion = False
        error = False
        if producto != None:
            if codigo != "" and nombre != "" and descripcion != "" and valor != 0 and unidadesExistentes != 0 and unitaria != 0 and request.POST['cantidad'] != "" and request.POST['proveedor'] != "" and cantidad_media != 0.0 and tiempo != 0 and errNum == False:
                if producto.codigo != codigo or producto.nombre != nombre:
                    try:
                        Producto.objects.get(codigo=codigo)
                        if producto.codigo != codigo:
                            error = True
                        else:
                            try:
                                Producto.objects.get(nombre=nombre)
                                if producto.nombre != nombre:
                                    error = True
                                else:
                                    modificacion = True
                            except ObjectDoesNotExist:
                                modificacion = True

                    except ObjectDoesNotExist:
                        modificacion = True
                        try:
                            Producto.objects.get(nombre=nombre)
                            if producto.nombre != nombre:
                                error = True
                            else:
                                modificacion = True
                        except ObjectDoesNotExist:
                            modificacion = True

                elif producto.codigo == codigo and producto.nombre == nombre:
                    modificacion = True

                if error:
                    mensaje="El insumo/reactivo con el codigo o nombre ingresado ya existe."
                else:
                    if modificacion == True:
                        proveedor = Usuario.objects.filter(id=request.POST['proveedor']).first()
                        if proveedor.first_name == "Interno (recurso propio)":
                            frecuencia_media = "NA"
                            frecuencia_minima = "NA"
                            cantidad_media = 0.0
                            tiempo = 0
                            stock_seguridad = 0.0
                            punto_pedido = 0.0

                        else:
                            stock_seguridad = views_nivel_insumos.calcularStockSeguridad(frecuencia_minima,cantidad_media, tiempo,numero_minimo_veces)
                            punto_pedido = views_nivel_insumos.calcularPuntoPedido(stock_seguridad, frecuencia_media,cantidad_media, tiempo,numero_medio_veces)

                        producto.codigo = codigo
                        producto.nombre = nombre
                        producto.descripcion = descripcion
                        producto.valorUnitario = valor
                        producto.unidadesExistentes = unidadesExistentes
                        producto.clasificacion = clasificacion
                        producto.unidad_medida = Tipo.objects.filter(id=request.POST['medida']).first()
                        producto.unidad_unitaria = unitaria
                        if (imageFile != None):
                            producto.imageFile = imageFile
                        producto.proveedor = proveedor
                        producto.frecuencia_media_uso = frecuencia_media
                        producto.frecuencia_minima_uso = frecuencia_minima
                        producto.cantidad_media_uso = cantidad_media
                        producto.tiempo_reaprovisionamiento = tiempo
                        producto.stock_seguridad = stock_seguridad
                        producto.punto_pedido = punto_pedido
                        producto.save()
                        mensaje = "ok"

            else:
                mensaje = "Todos los campos deben estar debidamente diligenciados"
        else:
            mensaje = "El id del insumo/reactivo que se quiere editar no existe"

    return JsonResponse({"mensaje": mensaje})