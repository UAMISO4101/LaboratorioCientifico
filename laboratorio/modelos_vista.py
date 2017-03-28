import json
import decimal
import datetime

class BodegaVista():
    id = 0
    serial = ""
    nombre = ""
    ubicacion = ""
    niveles = 0
    secciones = 0
    temperatura_minima = ""
    temperatura_media = ""
    estado = ""
    tipo_bodega = ""
    responsable = ""


class ProductosBodegaVista():
    id = 0
    bodega = ""
    producto = ""
    nivel = 0
    seccion = 0
    cantidad = 0
    unidad_medida = ""

class Convertidor(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__


class RecursoBusquedaVista():
    id = 0
    nombre = ""
    unidadesExistentes=""
    unidad_medida=""
    fechaTransaccion=""
    bodegaActual=""


class RecursoBusquedaDetalleVista():
    id=0
    fecha = ""
    recurso = ""
    tipoTransaccion = ""
    bodegaOrigen = ""
    bodegaDestino = ""
    usuario = ""
    autoriza = ""
    comentarios = ""


class ProductoVista():
    id = 0
    codigo = ""
    nombre = ""
    prod_id = ""
    descripcion = ""
    valorUnitario = 0
    unidadesExistentes = 0
    clasificacion = ""
    unidad_medida = ""
    unidad_unitaria = ""
    imageFile = ""

# HU-LCINV-13
# GZ
# Vista para formatear los datos a presentar en el UI
class TransaccionVista():
    id = 0
    tipo = ""
    bodega_origen = ""
    nivel_origen = 0
    seccion_origen = 0
    bodega_destino = ""
    nivel_destino = 0
    seccion_destino = 0
    producto = ""
    cantidad = 0
    unidad_medida = ""
    estado = ""
    fecha_creacion = ""
    fecha_ejecucion = ""
    comentarios = ""
    usuario = ""

# HU-LCINV-13
# GZ
# Manejo de fechas en formato ISO para presentar en el UI

def json_default(value):
    if isinstance(value, datetime.date):
        return datetime.date.isoformat(value)
    else:
        return value.__dict__