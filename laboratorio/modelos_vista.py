import json


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
    descripcion = ""
    valorUnitario = 0
    unidadesExistentes = 0
    clasificacion = ""
    unidad_medida = ""
    unidad_unitaria = ""
    imageFile = ""