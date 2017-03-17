import decimal
from datetime import datetime

from decimal import Decimal
from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from laboratorio.models import Tipo, Usuario, Bodega


def ir_index(request):
    return render(request,"laboratorio/index.html")
def ir_pie(request):
    return render(request,"laboratorio/pie.html")
def ir_encabezado(request):
    return render(request,"laboratorio/encabezado.html")
def ir_crear_bodega(request):
    return render(request, "laboratorio/crearBodega.html")

@csrf_exempt
def obtenerTiposBodega(request):
    qs = Tipo.objects.all()
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
            dosLugares = Decimal('00.01')
            bodega.temperatura_minima.quantize(dosLugares, 'ROUND_DOWN')
            bodega.temperatura_media.quantize(dosLugares, 'ROUND_DOWN')
            bodega.save()
            mensaje = "ok"
        else:
            mensaje = "La bodega con ese serial ya existe"

    return JsonResponse({"mensaje": mensaje})