import decimal
from django.db import connection
from datetime import datetime

from decimal import Decimal
from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from laboratorio.models import Tipo, Usuario, Bodega, Producto


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

@csrf_exempt
def busquedaProducto(request):
    qs = Producto.objects.all()
    #qs = Producto.objects.filter(unidad_medida__nombre__icontains="UM").order_by("nombre")
    #name_map = {'first': 'first_name', 'last': 'last_name', 'bd': 'birth_date', 'pk': 'id'}
    #qs = Producto.objects.raw("select* from laboratorio_producto where unidadesaExistentes=10")

    #sql_query = "SELECT* FROM LABORATORIO_PRODUCTO WHERE UNIDADESEXISTENTES=10"
    #required_question_information = Producto.objects.raw(sql_query)

    #cursor = connection.cursor()


    #qs2 = Bodega.objects.all()
    #qs3 = Bodega.objects.all()


    #mensajes = Mensaje.objects.filter(emisor=request.user) | | Mensaje.objects.filter(destinatarios__mensaje__emisor=request.user)
    #for especie in qs:
    #    especie.categoria_id = Categoria.objects.filter(id = especie.categoria_id).first().nombre
    qs_json = serializers.serialize('json', qs)

    return JsonResponse(qs_json, safe=False)


@csrf_exempt
def verProductoLista(request):
    #global globvar
    #globvar = request.GET.get('id');
    busquedaProducto(request)
    #consultar_especie_comentario(request)
    return render(request, "laboratorio/busquedaproducto.html")