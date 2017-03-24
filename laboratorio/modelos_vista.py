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

