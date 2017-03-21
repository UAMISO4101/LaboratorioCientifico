import decimal
import json
import time
from datetime import datetime

from decimal import Decimal
from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from laboratorio.modelos_vista import BodegaVista, Convertidor
from laboratorio.models import Tipo, Usuario, Bodega, Producto


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
def ir_recursos(request):
    return render(request, "laboratorio/recursos.html")
def ir_regitrarInsumos(request):
    return render(request, "laboratorio/registroInsumos.html")

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
def registrarInsumoReactivo(request):
    mensaje = ""
    dosLugares = Decimal('00.01')
    if request.method == 'POST':
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        valor = int(request.POST['valor'])
        unidadesExistentes = int(request.POST['unidades'])
        clasificacion = request.POST['clasificacion']
        unitaria = Decimal(request.POST['cantidad'])
        imageFile = request.FILES['imageFile']

        if Producto.objects.filter(codigo=codigo).first() != None:
            mensaje = "El insumo/reactivo con el codigo ingresado ya existe"
        else:
            if Producto.objects.filter(nombre=nombre).first() != None:
                mensaje = "El insumo/reactivo con el nombre ingresado ya existe"
            else:
                #Es un producto con un codigo y un nombre nuevos
                producto = Producto(codigo=codigo,
                                    nombre=nombre,
                                    descripcion=descripcion,
                                    valorUnitario=valor,
                                    unidadesExistentes=unidadesExistentes,
                                    clasificacion=clasificacion,
                                    unidad_medida=Tipo.objects.filter(id=request.POST['medida']).first(),
                                    unidad_unitaria=unitaria,
                                    imageFile=imageFile)

                producto.unidad_unitaria.quantize(dosLugares, 'ROUND_DOWN')
                producto.save()
                mensaje = "ok"

    return JsonResponse({"mensaje":mensaje})

@csrf_exempt
def obtenerTiposMedida(request):
    qs = Tipo.objects.filter(grupo="MEDIDAPRODUCTO")
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)