import decimal
import json
import time
from datetime import datetime

from decimal import Decimal

import sys
from django.core import serializers
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from psycopg2.extensions import JSON

from laboratorio.modelos_vista import BodegaVista, Convertidor
from laboratorio.modelos_vista import ProductosBodegaVista

from laboratorio.models import Tipo, Usuario, Bodega
from laboratorio.models import TransaccionInventario, Producto, ProductosEnBodega

def ir_index(request):
    return render(request,"laboratorio/index.html")
def ir_pie(request):
    return render(request,"laboratorio/pie.html")
def ir_encabezado(request):
    return render(request,"laboratorio/encabezado.html")
def ir_crear_bodega(request):
    return render(request, "laboratorio/crearBodega.html")
def ir_bodegas(request):
    return render(request, "laboratorio/bodegas.html")

def ir_crear_transaccion(request):
    return render(request,"laboratorio/crearTransaccion.html")

@csrf_exempt
def obtenerTiposBodega(request):
    qs = Tipo.objects.filter(grupo="BODEGA")
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)

@csrf_exempt
def obtenerUsuarios(request):
    qs = Usuario.objects.all()
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)

@csrf_exempt
def crearBodega(request):
    mensaje = ""
    if request.method == 'POST':
        dosLugares = Decimal('00.01')
        if request.POST['id_bodega_guardada'] == None or request.POST['id_bodega_guardada'] == "":
            bodega = Bodega(serial=request.POST['serial'],
                        nombre=request.POST['nombre'],
                        niveles=int(request.POST['niveles']),
                        secciones=int(request.POST['secciones']),
                        temperatura_minima=Decimal(request.POST['temperatura_minima']),
                        temperatura_media=Decimal(request.POST['temperatura_media']),
                        ubicacion = request.POST['ubicacion'],
                        fecha_creacion = datetime.now(),
                        tipo_bodega = Tipo.objects.filter(id=request.POST['tipo_bodega']).first(),
                        usuario=Usuario.objects.filter(id=request.POST['responsable']).first())

            if not Bodega.objects.filter(serial=bodega.serial).exists():
                bodega.temperatura_minima.quantize(dosLugares, 'ROUND_DOWN')
                bodega.temperatura_media.quantize(dosLugares, 'ROUND_DOWN')
                bodega.save()
                mensaje = "ok"
            else:
                mensaje = "La bodega con ese serial ya existe"
        else:
            bodegass = Bodega.objects.filter(id=int(request.POST['id_bodega_guardada']))
            if (bodegass.exists()):
                bodega = bodegass.first()
                bodega.serial=request.POST['serial']
                bodega.nombre=request.POST['nombre']
                bodega.niveles = int(request.POST['niveles'])
                bodega.secciones = int(request.POST['secciones'])
                bodega.temperatura_minima =Decimal(request.POST['temperatura_minima'])
                bodega.temperatura_media =Decimal(request.POST['temperatura_media'])
                bodega.ubicacion = request.POST['ubicacion']
                bodega.tipo_bodega = Tipo.objects.filter(id=request.POST['tipo_bodega']).first()
                bodega.usuario = Usuario.objects.filter(id=request.POST['responsable']).first()

                bodegaBDs = Bodega.objects.filter(serial=bodega.serial)
                actualizar = True
                if bodegaBDs.exists() and bodega.id != bodegaBDs.first().id:
                    actualizar = False

                if actualizar:
                    bodega.temperatura_minima.quantize(dosLugares, 'ROUND_DOWN')
                    bodega.temperatura_media.quantize(dosLugares, 'ROUND_DOWN')
                    bodega.fecha_actualizacion = datetime.now()
                    bodega.save()
                    mensaje = "ok"
                else:
                    mensaje = "La bodega con ese serial ya existe"



    return JsonResponse({"mensaje": mensaje})

@csrf_exempt
def obtenerBodegas(request):
    qs = Bodega.objects.all()
    listaBodegas = []
    for bodega in qs:
        bod = BodegaVista()
        bod.id = bodega.id
        bod.nombre = bodega.nombre
        bod.serial = bodega.serial
        bod.niveles = bodega.niveles
        bod.secciones = bodega.secciones
        bod.temperatura_minima = str(bodega.temperatura_minima)
        bod.temperatura_media = str(bodega.temperatura_media)
        bod.ubicacion = bodega.ubicacion
        bod.tipo_bodega = bodega.tipo_bodega.nombre
        if bodega.estado:
            bod.estado = "Activo"
        else:
            bod.estado = "Inactivo"
        bod.responsable = bodega.usuario.first_name + " " + bodega.usuario.last_name
        listaBodegas.append(bod)
    json_string = json.dumps(listaBodegas, cls=Convertidor)
    return JsonResponse(json_string, safe=False)

@csrf_exempt
def obtenerBodega(request):
    time.sleep(0.3)
    qs = Bodega.objects.filter(id=request.GET['id_bodega'])
    qs_json = serializers.serialize('json', qs)
    struct = json.loads(qs_json)
    json_bodega = json.dumps(struct[0])
    return JsonResponse({"bodega": json_bodega})



@csrf_exempt
def crear_transaccion(request):
    if request.method == 'POST':
        json_tran = json.loads(request.body);

        transaccion = TransaccionInventario(
            tipo=Tipo.objects.get(pk=json_tran['tipo']),
            bodega_origen= Bodega.objects.get(pk=json_tran['bodega_origen']),
            nivel_origen=json_tran['nivel_origen'],
            seccion_origen=json_tran['seccion_origen'],
            bodega_destino = Bodega.objects.get(pk=json_tran['bodega_destino']),
            nivel_destino=json_tran['nivel_origen'],
            seccion_destino=json_tran['seccion_origen'],
            producto_bodega_origen = ProductosEnBodega.objects.get(pk=json_tran['producto_bodega_origen']),
            #producto=Producto.objects.get(pk=json_tran['producto']),
            cantidad=json_tran['cantidad'],
            unidad_medida=Tipo.objects.get(nombre=json_tran['unidad_medida']),
            #estado=Tipo.objects.filter(id=json_tran['estado']),
            fecha_creacion=datetime.now(),
            fecha_ejecucion=datetime.now(),
            usuario=Usuario.objects.get(pk=1),
            comentarios=json_tran['comentarios']
        )
        ejecutar_transaccion(transaccion)
        transaccion.save()
        tran_json = json.loads(serializers.serialize('json', [transaccion]));
        return JsonResponse(tran_json, safe=False)





def ejecutar_transaccion(transaccion):
    try:
        print >> sys.stdout, "EN EJECUCION" + str(json.loads(serializers.serialize('json', [transaccion])))
        print >> sys.stdout, "CAMPOS:" + transaccion.comentarios
        print >> sys.stdout, "CAMPOS:" + str(transaccion.producto)
        producto_bodega_origen = ProductosEnBodega.objects.get(pk=transaccion.producto_bodega_origen.pk)
        print >> sys.stdout, "BDDESTINO:" + str(transaccion.bodega_destino)

        producto_bodega_destino_list = ProductosEnBodega.objects.filter(bodega=transaccion.bodega_destino)
        producto_bodega_origen.cantidad = int(producto_bodega_origen.cantidad) - int(transaccion.cantidad)
        if producto_bodega_destino_list.exists():
            producto_bodega_destino = producto_bodega_destino_list.first()
            print >> sys.stdout, "SI HAY EN DESTINO"
            producto_bodega_destino.cantidad = int(producto_bodega_destino.cantidad) + int(transaccion.cantidad)
            print >> sys.stdout, "CANTIDAD:" + str(producto_bodega_origen.cantidad)
        else:
            producto_bodega_destino = ProductosEnBodega(
                                    bodega=transaccion.bodega_destino,
                                    producto = producto_bodega_origen.producto,
                                    nivel = transaccion.nivel_destino,
                                    seccion = transaccion.seccion_destino,
                                    cantidad = transaccion.cantidad,
                                    unidad_medida=transaccion.unidad_medida

            )

        producto_bodega_destino.save();
        producto_bodega_origen.save()


    except Exception as e:
        print 'EXCEPCION: %s (%s)' % (e.message, type(e))


#Funcion GET que trae listas de valores segun el tipo
@csrf_exempt
def obtenerTipos(request):
    grupo = request.GET['grupo']
    qs = Tipo.objects.filter(grupo=grupo)
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)


# Obtiene los productos de la bodega seleccionada
@csrf_exempt
def obtenerProductosBodega(request):
    bodega = request.GET['bodega']
    pb_bodAll = ProductosEnBodega.objects.filter(bodega=Bodega.objects.get(pk=bodega))
    pb_bod = pb_bodAll.filter(cantidad__gt=0)
    listaProductosBodegas = []

    for productoBodega in pb_bod:
        pb = ProductosBodegaVista()
        pb.id = productoBodega.id
        pb.bodega = productoBodega.bodega.pk
        pb.producto = Producto.objects.get(pk=productoBodega.producto.pk).nombre
        pb.cantidad = productoBodega.cantidad
        pb.nivel = productoBodega.nivel
        pb.seccion = productoBodega.seccion
        pb.unidad_medida = Tipo.objects.get(pk=productoBodega.unidad_medida.id).nombre
        listaProductosBodegas.append(pb)
    json_pb = json.dumps(listaProductosBodegas, cls=Convertidor)
    return JsonResponse(json_pb, safe=False)




