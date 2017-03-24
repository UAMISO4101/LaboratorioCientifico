import decimal
import json
import time
from datetime import datetime

from decimal import Decimal
from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from laboratorio.models import Tipo, Usuario, Bodega, Producto, TransaccionInventario
from laboratorio.modelos_vista import BodegaVista, Convertidor, RecursoBusquedaVista, RecursoBusquedaDetalleVista
from laboratorio.models import Tipo, Usuario, Bodega


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
        if request.POST.get('id_bodega_guardada', None) == None or request.POST.get('id_bodega_guardada', None) == "":
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
def busquedaProducto(request):
    #Capturar el valor de los campos

    #Crear la expresion Q

    #Filtra por la expresion; si no hay nada, muestra todos los productos
    if True:
        qs = Producto.objects.all()
    else:
        qs = Producto.objects.all() #filtro


    listaRecurso = []

    for recurso in qs:
        req = RecursoBusquedaVista()
        req.id = recurso.id
        req.nombre = recurso.nombre
        req.unidadesExistentes = recurso.unidadesExistentes
        req.unidad_medida = recurso.unidad_medida.nombre
        req.fechaTransaccion =  obtenerBodegaAcutalxRecurso(recurso, 2)
        req.bodegaActual=obtenerBodegaAcutalxRecurso(recurso, 1)
        listaRecurso.append(req)

    json_string = json.dumps(listaRecurso, cls=Convertidor)

    return JsonResponse(json_string, safe=False)


def obtenerBodegaAcutalxRecurso(recurso, campo):
    qs = TransaccionInventario.objects.filter(producto=recurso).order_by('-fecha_ejecucion')[:1]

    retorno="N/A"

    if qs.first():
        #retorno = serializers.serialize('json', qs)
        if campo==1:
            retorno=qs[0].bodega_destino.nombre
        if campo==2:
            retorno = str(qs[0].fecha_ejecucion)
    return retorno


def obtenerNombreUsuarioxId(usuario):
    qs = Usuario.objects.filter(id=usuario)[:1]

    retorno="N/A"

    #if qs.first():
    retorno=qs[0].first_name + " " + qs[0].last_name

    return retorno


@csrf_exempt
def busquedaProductoDetalle(request):
    qs = TransaccionInventario.objects.filter(producto_id=1).order_by('-fecha_creacion')

    listaTrans = []

    for transaccion in qs:
        req = RecursoBusquedaDetalleVista()
        req.id = transaccion.id
        req.fecha = str(transaccion.fecha_ejecucion)
        req.recurso = transaccion.producto.nombre
        req.tipoTransaccion = transaccion.tipo.nombre
        req.bodegaOrigen = transaccion.producto_bodega_origen.bodega.nombre
        req.bodegaDestino = transaccion.producto_bodega_destino.bodega.nombre
        req.usuario = transaccion.usuario.first_name + " " + transaccion.usuario.last_name
        req.autoriza = transaccion.autoriza.first_name + " " + transaccion.autoriza.last_name
        #req.usuario = obtenerNombreUsuarioxId(            transaccion.usuario.id)
        #req.autoriza = obtenerNombreUsuarioxId(            transaccion.autoriza.id)
        req.comentarios = transaccion.comentarios
        listaTrans.append(req)

    json_string = json.dumps(listaTrans, cls=Convertidor)

    #json_string = serializers.serialize('json', qs)

    return JsonResponse(json_string, safe=False)

#def llenarElementos:



@csrf_exempt
def verProductoBusqueda(request):
    #llenarElementos(request)
    busquedaProducto(request)
    return render(request, "laboratorio/busquedaproducto.html")


@csrf_exempt
def verProductoBusquedaDetalle(request):
    global globvar
    globvar = request.GET.get('id');
    busquedaProductoDetalle(request)
    return render(request, "laboratorio/busquedaproductodetalle.html")

  
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