import json

import decimal


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