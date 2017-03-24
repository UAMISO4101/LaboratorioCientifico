# coding=utf-8

import decimal
import json
import time
from datetime import datetime

from decimal import Decimal

import sys
from django.core import serializers

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse, HttpResponse

from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from psycopg2.extensions import JSON


from laboratorio.modelos_vista import BodegaVista, Convertidor, ProductoVista, ProductosBodegaVista, TransaccionVista, json_default
from laboratorio.models import Tipo, Usuario, Bodega, Experimento, ProductoProtocolo, Producto, Protocolo

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
def ir_recursos(request):
    return render(request, "laboratorio/recursos.html")
def ir_regitrarInsumos(request):
    return render(request, "laboratorio/registroInsumos.html")
def ir_ver_recursos(request):
    return render(request, "laboratorio/verRecursos.html")
def ir_editarRecurso(request, recurso_id=1):
    return render(request, "laboratorio/edicionInsumos.html")

def ir_crear_transaccion(request):
    return render(request,"laboratorio/crearTransaccion.html")

def ir_transacciones(request):
    return render(request,"laboratorio/transacciones.html")


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
def obtenerTransacciones(request):
    qs = TransaccionInventario.objects.all()
    listaTransacciones = []
    for transaccion in qs:
        trx = TransaccionVista()
        trx.id = transaccion.id
        trx.tipo = transaccion.tipo.nombre
        trx.bodega_origen = transaccion.bodega_origen.nombre
        trx.nivel_origen = transaccion.nivel_origen
        trx.seccion_origen = transaccion.seccion_origen
        trx.bodega_destino = transaccion.bodega_destino.nombre
        trx.nivel_destino = transaccion.nivel_destino
        trx.seccion_destino = transaccion.seccion_destino
        trx.producto = transaccion.producto.nombre
        trx.cantidad = transaccion.cantidad
        trx.unidad_medida = transaccion.unidad_medida.nombre
        trx.estado = transaccion.estado.nombre
        trx.fecha_creacion = transaccion.fecha_creacion
        trx.fecha_ejecucion = transaccion.fecha_ejecucion
        trx.comentarios = transaccion.comentarios
        trx.usuario = transaccion.usuario
        #bod.responsable = bodega.usuario.first_name + " " + bodega.usuario.last_name
        listaTransacciones.append(trx)
    json_string = json.dumps(listaTransacciones, cls=Convertidor, ensure_ascii=False, default=json_default)
    return JsonResponse(json_string, safe=False)

@csrf_exempt
def obtenerTransaccion(request):
    time.sleep(0.3)
    qs = TransaccionInventario.objects.filter(id=request.GET['id_transaccion'])
    qs_json = serializers.serialize('json', qs)
    struct = json.loads(qs_json)
    json_bodega = json.dumps(struct[0])
    return JsonResponse({"transaccion": json_bodega})
  
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
        print >> sys.stdout, "Prod" + json_tran['producto']
        print >> sys.stdout, "PRODProd" + json_tran['producto_bodega_origen']
        transaccion = TransaccionInventario(
            tipo=Tipo.objects.get(pk=json_tran['tipo']),
            bodega_origen= Bodega.objects.get(pk=json_tran['bodega_origen']),
            nivel_origen=json_tran['nivel_origen'],
            seccion_origen=json_tran['seccion_origen'],
            bodega_destino = Bodega.objects.get(pk=json_tran['bodega_destino']),
            nivel_destino=json_tran['nivel_destino'],
            seccion_destino=json_tran['seccion_destino'],
            producto_bodega_origen = ProductosEnBodega.objects.get(pk=json_tran['producto_bodega_origen']),
            producto=Producto.objects.get(pk=json_tran['producto']),
            cantidad=json_tran['cantidad'],
            unidad_medida=Tipo.objects.get(nombre=json_tran['unidad_medida']),
            estado=Tipo.objects.get(pk=Tipo.objects.filter(nombre='Ejecutada').first().id),
            fecha_creacion=datetime.now(),
            fecha_ejecucion=datetime.now(),
            usuario=Usuario.objects.get(pk=1),
            comentarios=json_tran['comentarios']
        )
        ejecutar_transaccion(transaccion)
        transaccion.save()
        tran_json = json.loads(serializers.serialize('json', [transaccion]));
        return JsonResponse(tran_json, safe=False)
      
@csrf_exempt
def ejecutar_transaccion(transaccion):
    try:
        if transaccion.tipo.nombre != "Recepcion de Proveedor":
            producto_bodega_origen = ProductosEnBodega.objects.get(pk=transaccion.producto_bodega_origen.pk)
            producto_bodega_origen.cantidad = int(producto_bodega_origen.cantidad) - int(transaccion.cantidad)
            producto = producto_bodega_origen.producto
        else:
            producto = transaccion.producto


        producto_bodega_destino_list = ProductosEnBodega.objects.filter(bodega=transaccion.bodega_destino)
        producto_bodega_destino_list = producto_bodega_destino_list.filter(producto=transaccion.producto)
        producto_bodega_destino_list = producto_bodega_destino_list.filter(nivel=transaccion.nivel_destino)
        producto_bodega_destino_list = producto_bodega_destino_list.filter(seccion=transaccion.seccion_destino)

        if producto_bodega_destino_list.exists():
            producto_bodega_destino = producto_bodega_destino_list.first()
            producto_bodega_destino.cantidad = int(producto_bodega_destino.cantidad) + int(transaccion.cantidad)
        else:
            producto_bodega_destino = ProductosEnBodega(
                                    bodega=transaccion.bodega_destino,
                                    producto = producto,
                                    nivel = transaccion.nivel_destino,
                                    seccion = transaccion.seccion_destino,
                                    cantidad = transaccion.cantidad,
                                    unidad_medida=transaccion.unidad_medida

            )

        producto_bodega_destino.save()
        transaccion.fecha_ejecucion=datetime.now()
        transaccion.producto_bodega_destino = producto_bodega_destino
        transaccion.estado = Tipo.objects.get(pk=Tipo.objects.filter(nombre='Ejecutada').first().id)
        transaccion.save()
        if transaccion.tipo.nombre != "Recepcion de Proveedor":
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
        pb.prod_id = Producto.objects.get(pk=productoBodega.producto.pk).pk
        pb.cantidad = productoBodega.cantidad
        pb.nivel = productoBodega.nivel
        pb.seccion = productoBodega.seccion
        pb.unidad_medida = Tipo.objects.get(pk=productoBodega.unidad_medida.id).nombre
        listaProductosBodegas.append(pb)
    json_pb = json.dumps(listaProductosBodegas, cls=Convertidor)
    return JsonResponse(json_pb, safe=False)        
        
        
@csrf_exempt
def obtenerExperimentos(request):
    qs = Experimento.objects.all().prefetch_related('asignado')
    qs_json = serializers.serialize('json', qs)
    respT = []
    for exp in qs:
        asignado = exp.asignado.values('username', 'id')[0]
        struct = json.loads(qs_json)[0]
        resp = {'experimento': struct, 'asignado': asignado}
        respT.append(resp)
    return JsonResponse(respT, safe=False)

@csrf_exempt
def obtenerExperimentosPorUsuario(request):
    usuario = Usuario.objects.get(username=request.GET['username'])
    exp_usuario = Experimento.objects.filter(asignado=usuario)
    qs_json = serializers.serialize('json', exp_usuario)
    return JsonResponse(qs_json, safe=False)

@csrf_exempt
def obtenerProtocolosPorExperimento(request):
    exp = Experimento.objects.filter(codigo=request.GET['codigo'])
    prots_exp = Protocolo.objects.filter(experimento=exp)
    qs_json = serializers.serialize('json', prots_exp)
    return JsonResponse(qs_json, safe=False)

@csrf_exempt
def obtenerPPPorProtocolo(request):
    prot = Protocolo.objects.filter(id=request.GET['id'])
    prods_prot = ProductoProtocolo.objects.filter(protocolo=prot).select_related('producto')
    qs_json = serializers.serialize('json', prods_prot)
    producto = {'nombre':prods_prot.first().producto.nombre,
                'id': prods_prot.first().producto.pk}
    struct = json.loads(qs_json)[0]
    resp = {'productoprotocolo': struct, 'producto': producto}
    return JsonResponse(resp, safe=False)

def experimentos(request):
    return render(request, "laboratorio/experimentos.html")

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

        if Producto.objects.filter(codigo=codigo).first() != None or Producto.objects.filter(nombre=codigo).first() !=None:
            mensaje = "El insumo/reactivo con el codigo o nombre ingresado ya existe."
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
        listaProductos.append(prod)
    json_string = json.dumps(listaProductos, cls=Convertidor)
    return JsonResponse(json_string, safe=False)

@csrf_exempt
def obtenerRecurso(request):
    time.sleep(0.3)
    qs = Producto.objects.filter(id=request.GET['recurso_id'])
    qs_json = serializers.serialize('json', qs)
    struct = json.loads(qs_json)
    json_recurso = json.dumps(struct[0])
    return JsonResponse({"producto": json_recurso})

@csrf_exempt
def guardarEdicionInsumo(request):

    mensaje = ""
    if request.method == 'POST':
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        valor = int(request.POST['valor'])
        unidadesExistentes = int(request.POST['unidades'])
        clasificacion = request.POST['clasificacion']
        unitaria = Decimal(request.POST['cantidad'])
        imageFile = request.FILES.get('imageFile',None)

        producto = Producto.objects.filter(id=int(request.POST['id_producto_guardado'])).first()


        modificacion = False
        error = False
        if producto != None:

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
                    producto.save()
                    mensaje = "ok"

        else:
            mensaje = "El id del insumo/reactivo que se quiere editar no existe"

    return JsonResponse({"mensaje": mensaje})
