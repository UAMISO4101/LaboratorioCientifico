import json
import decimal
import datetime

"""Clase - Auxiliar  BodegaVista.
Clase que sirve de vista para objetos a mostrar al usuario
"""
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
    unidad_medida = ""

"""Clase - Auxiliar  ProductosBodegaVista.
Clase que sirve de vista para objetos a mostrar al usuario
"""
class ProductosBodegaVista():
    id = 0
    bodega = ""
    producto = ""
    nivel = 0
    seccion = 0
    cantidad = 0
    unidad_medida = ""

"""Clase -  Convertidor.
Clase que sirve como convertidor de json a objeto
"""
class Convertidor(json.JSONEncoder):
    """Metodo por defecto de la clase.
    """
    def default(self, obj):
        return obj.__dict__

"""Clase - Auxiliar  RecursoBusquedaVista.
Clase que sirve de vista para objetos a mostrar al usuario
"""
class RecursoBusquedaVista():
    id = 0
    nombre = ""
    unidadesExistentes = ""
    unidad_medida = ""
    fechaTransaccion = ""  # Fecha en string
    bodegaActual = ""
    hidden1 = ""
    cantidad_convertida = ""

"""Clase - Auxiliar  RecursoBusquedaDetalleVista.
Clase que sirve de vista para objetos a mostrar al usuario
"""
class RecursoBusquedaDetalleVista():
    id=0
    fecha = ""
    recurso = ""
    tipoTransaccion = ""  # TIPOTRX
    bodegaOrigen = ""
    nivel_origen = ""
    seccion_origen = ""
    bodegaDestino = ""
    nivel_destino = ""
    seccion_destino = ""
    cantidad = ""
    unidad_medida = ""
    usuario = ""
    autoriza = ""
    comentarios = ""
    estadoTrans = ""  # STATUSTRX

"""Clase - Auxiliar  ProductoVista.
Clase que sirve de vista para objetos a mostrar al usuario
"""
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
    proveedor = ""
    frecuencia_media = ""
    frecuencia_minima = ""
    cantidad_media = ""
    tiempo_reaprovisionamiento = ""

"""Clase - Auxiliar  TransaccionVista.
Clase que sirve de vista para objetos a mostrar al usuario
"""
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

"""Clase - Auxiliar  OrdenPedidoVista.
Clase que sirve de vista para objetos a mostrar al usuario
"""
class OrdenPedidoVista():
    id = 0
    nombreUsuarioCreacion = ""
    nombreUsuarioAprobacion = ""
    nombreProveedor = ""
    estado = ""
    fechaPeticion = ""

"""Clase - Auxiliar  OrdenPedidoVista.
Clase que sirve de vista para objetos a mostrar al usuario
"""
class DetalleOrdenVista():
    idProducto = 0;
    nombreProducto = "";
    idBodega = 0;
    nombreBodega = "";
    nivel = 0;
    seccion = 0;
    valorUnitario = 0.0;
    cantidad = 0.0;
    fechaMovimiento = None;
    transaccion_inventario=0;
    estado="";

# HU-LCINV-13
# GZ
# Manejo de fechas en formato ISO para presentar en el UI
"""Metodo que formatea a json
"""
def json_default(value):
    if isinstance(value, datetime.date):
        return datetime.date.isoformat(value)
    else:
        return value.__dict__


# LCINV-7
# FB
# Manejo para el vencimiento de productos
class ProductoVencimientoVista():
    id = 0
    bodega = ""
    producto = ""
    nivel = 0
    seccion = 0
    fecha_vencimiento = ""
    dias_anticipacion = ""
    semaforo_vencimiento = ""
